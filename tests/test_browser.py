"""Real browser tests. Missing Chromium is a failure, never an automatic skip."""
from proofrunner.demo import JOURNEY, demo_server
from proofrunner.planner import controlled_plan
from proofrunner.runner import execute

def test_real_login_cart_and_evidence(tmp_path, monkeypatch):
    monkeypatch.setenv("PR_TEST_PASSWORD", "demo-pass")
    with demo_server() as url:
        path, run = execute(url, controlled_plan(JOURNEY), output=tmp_path,
                            interactions=True, local_demo=True)
    assert run["result"] == "PASS", run.get("error", run["steps"])
    assert len(list((path / "screenshots").glob("*.png"))) == 7
    assert "demo-pass" not in (path / "execution.json").read_text()

def test_real_broken_cart_fails_and_skips_remainder(tmp_path, monkeypatch):
    monkeypatch.setenv("PR_TEST_PASSWORD", "demo-pass")
    with demo_server() as url:
        path, run = execute(url + "?broken=1", controlled_plan(JOURNEY), output=tmp_path,
                            interactions=True, local_demo=True, timeout=700)
    assert run["result"] == "FAIL", run.get("error", run["steps"])
    assert run["steps"][5]["status"] == "FAIL"
    assert run["steps"][6]["status"] == "SKIPPED"
    assert run["steps"][5]["expected"] == "1"
    assert (path / run["steps"][5]["screenshot"]).is_file()

def test_read_only_blocks_click_before_it_happens(tmp_path):
    with demo_server() as url:
        _, run = execute(url, controlled_plan('Click "Sign In"\nVerify visible "Dashboard"'),
                         output=tmp_path, local_demo=True)
    assert run["result"] == "ERROR"
    assert "Interaction requires" in run["steps"][0]["observed"]
    assert run["steps"][1]["status"] == "SKIPPED"
