import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

from .report import write_reports
from .safety import Policy, SafetyError, redact, safe_url
from .schema import Step, parse_plan

def utcnow():
    return datetime.now(timezone.utc).isoformat()

def resolve(page, step, planner=None, secrets=()):
    by, target = step["by"], step["target"]
    if by == "label":
        return page.get_by_label(target, exact=True), step
    if by == "role":
        return page.get_by_role(step["role"], name=target, exact=True), step
    if by == "text":
        return page.get_by_text(target, exact=True), step
    if by == "testid":
        return page.get_by_test_id(target), step
    candidates = [("label", "", page.get_by_label(target, exact=True)),
                  ("testid", "", page.get_by_test_id(target))]
    for role in ("button", "link", "heading", "textbox", "checkbox", "combobox", "status"):
        candidates.append(("role", role, page.get_by_role(role, name=target, exact=True)))
    candidates.append(("text", "", page.get_by_text(target, exact=True)))
    # Auto resolution only accepts a unique, visible match. Never choose .first.
    for strategy, role, locator in candidates:
        if locator.count() == 1 and locator.is_visible():
            return locator, {**step, "by":strategy, "role":role}
    if planner:
        snapshot = redact(page.locator("body").aria_snapshot()[:18000], secrets)
        resolved = {**step, **planner.locate(step, snapshot)}
        return resolve(page, resolved, secrets=secrets)
    # Explicit strategies wait via Playwright assertions/actions; auto resolution
    # with no model requires an already present unambiguous element.
    raise LookupError(f"No unique visible element: {target}")

def screenshot(page, path, secrets):
    # Mask input values AND any DOM text nodes that echo supplied secrets.
    masks = [page.locator("input, textarea, [contenteditable=true]")]
    masks.extend(page.get_by_text(secret, exact=False) for secret in secrets if secret)
    page.screenshot(path=str(path), full_page=True, mask=masks, timeout=5000,
                    animations="disabled")

def execute(url, plan, *, output="runs", prompt="", planner=None,
            planner_name="structured", interactions=False, local_demo=False, timeout=5000):
    plan = parse_plan(plan)
    secrets = [os.environ[s["value"]] for s in plan["steps"]
               if s["action"] == "fill_secret" and os.environ.get(s["value"])]
    # Check prompt/plan logs against explicitly supplied test secrets before persisting.
    directory = Path(output) / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8])
    (directory / "screenshots").mkdir(parents=True)
    start = time.monotonic()
    run = {"version":1, "name":plan["name"], "url":safe_url(url), "started":utcnow(),
           "duration":0, "result":"ERROR", "planner":planner_name, "prompt":prompt,
           "plan":plan, "steps":[], "network_errors":[], "blocked_requests":[],
           "local_demo":local_demo}
    browser = None
    context = None
    pw = None
    page = None
    try:
        from playwright.sync_api import sync_playwright, expect, TimeoutError as BrowserTimeout
        policy = Policy(url, interactions=interactions, local_demo=local_demo)
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True,
            executable_path=os.environ.get("PROOFRUNNER_BROWSER_EXECUTABLE") or None)
        context = browser.new_context(accept_downloads=False, service_workers="block",
                                      viewport={"width":1280,"height":900})
        context.set_default_timeout(timeout)
        def route(request_route):
            request = request_route.request
            try:
                policy.check_url(request.url)
                if request.method not in {"GET", "HEAD", "OPTIONS"} and not interactions:
                    raise SafetyError("Write request blocked in read-only mode")
            except (SafetyError, OSError, ValueError) as error:
                run["blocked_requests"].append({"url":safe_url(request.url),"reason":str(error)})
                request_route.abort("blockedbyclient")
                return
            request_route.continue_()
        context.route("**/*", route)
        # WebSockets bypass ordinary HTTP routing; disable them explicitly.
        context.route_web_socket("**/*", lambda ws: ws.close())
        page = context.new_page()
        context.on("page", lambda popup: popup.close())
        page.on("dialog", lambda dialog: dialog.dismiss())
        page.on("download", lambda download: download.cancel())
        page.on("response", lambda response: run["network_errors"].append(
            {"url":safe_url(response.url), "status":response.status}) if response.status >= 400 else None)
        response = page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        if response and response.status >= 400:
            raise RuntimeError(f"Initial navigation returned HTTP {response.status}")
        halted = False
        for i, original in enumerate(plan["steps"], 1):
            step = dict(original)
            record = {**step, "status":"SKIPPED", "started":utcnow(), "duration":0,
                      "observed":"Not executed after previous failure"}
            run["steps"].append(record)
            if halted:
                continue
            tick = time.monotonic()
            try:
                op = step["action"]
                policy.check_action(step)
                if op == "navigate":
                    destination = urljoin(page.url, step["value"])
                    policy.check_url(destination)
                    response = page.goto(destination, wait_until="domcontentloaded")
                    if response and response.status >= 400:
                        raise AssertionError(f"Navigation returned HTTP {response.status}")
                    record["observed"] = safe_url(page.url)
                elif op == "assert_url":
                    expect(page).to_have_url(step["expected"], timeout=timeout)
                    record["observed"] = safe_url(page.url)
                else:
                    locator, grounded = resolve(page, step, planner, secrets)
                    record.update({k:grounded[k] for k in ("target", "by", "role")})
                    # Replay keeps the original exact expectation but records real locators.
                    run["plan"]["steps"][i-1].update({k:grounded[k] for k in ("target", "by", "role")})
                    descriptor = locator.evaluate("el => [el.innerText,el.getAttribute('aria-label'),el.getAttribute('href'),el.getAttribute('formaction'),el.closest('form')?.getAttribute('action')].filter(Boolean).join(' ')")
                    policy.check_action(step, descriptor)
                    if op == "click":
                        locator.click()
                        record["observed"] = "Click completed; see subsequent assertions for acceptance"
                    elif op in {"fill", "fill_secret"}:
                        if op == "fill" and locator.get_attribute("type") == "password":
                            raise SafetyError("Password fields require fill_secret with PR_TEST_* environment names")
                        value = step["value"]
                        if op == "fill_secret":
                            value = os.environ.get(value)
                            if not value:
                                raise ValueError("Missing test credential environment variable")
                        locator.fill(value)
                        record["observed"] = "Field filled (value omitted)"
                    elif op == "select":
                        locator.select_option(label=step["value"])
                        record["observed"] = "Option selected"
                    elif op in {"wait", "assert_visible"}:
                        expect(locator).to_be_visible(timeout=timeout)
                        record["observed"] = "Element visible"
                    elif op == "assert_enabled":
                        expect(locator).to_be_enabled(timeout=timeout)
                        record["observed"] = "Element enabled"
                    elif op == "assert_checked":
                        expect(locator).to_be_checked(timeout=timeout)
                        record["observed"] = "Element checked"
                    elif op == "read":
                        record["observed"] = locator.inner_text()[:2000]
                    elif op == "assert_text":
                        expect(locator).to_have_text(step["expected"], use_inner_text=True, timeout=timeout)
                        record["observed"] = locator.inner_text()[:2000]
                policy.check_url(page.url)
                record["status"] = "PASS"
            except (AssertionError, BrowserTimeout, LookupError) as error:
                record.update(status="FAIL", observed=str(error)[:3000])
                halted = True
            except Exception as error:
                record.update(status="ERROR", observed=f"{type(error).__name__}: {str(error)[:2000]}")
                halted = True
            finally:
                record["duration"] = round(time.monotonic()-tick, 3)
                record["url"] = safe_url(page.url)
                relative = f"screenshots/step-{i:02d}.png"
                try:
                    screenshot(page, directory / relative, secrets)
                    record["screenshot"] = relative
                except Exception:
                    record["evidence_error"] = "Screenshot unavailable"
                    record["status"] = "ERROR"
                    halted = True
                run["duration"] = time.monotonic()-start
                write_reports(directory, redact(run, secrets))
        states = {s["status"] for s in run["steps"]}
        run["result"] = "ERROR" if "ERROR" in states else "FAIL" if "FAIL" in states else "PASS"
    except Exception as error:
        run["error"] = f"{type(error).__name__}: {str(error)[:2000]}"
        run["result"] = "ERROR"
        if not run["steps"]:
            run["steps"] = [{**s,"status":"SKIPPED","observed":"Run failed before execution"} for s in plan["steps"]]
        if page:
            try:
                screenshot(page, directory / "screenshots/failure.png", secrets)
            except Exception:
                pass
    finally:
        for obj in (context, browser):
            if obj:
                try:
                    obj.close()
                except Exception:
                    pass
        if pw:
            pw.stop()
        run["duration"] = round(time.monotonic()-start, 3)
        run = redact(run, secrets)
        write_reports(directory, run)
    return directory, run
