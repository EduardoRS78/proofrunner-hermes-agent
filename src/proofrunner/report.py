import html
import json
from pathlib import Path

def write_reports(directory, run):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "execution.json").write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = ["# ProofRunner Test Report", "", f"**{run['result']}** — {run['name']}", "",
             f"Target: {run['url']}", f"Started: {run['started']}", f"Duration: {run['duration']:.2f}s",
             f"Planner: {run['planner']}", "", "## Steps", ""]
    for i,s in enumerate(run["steps"], 1):
        lines += [f"### {i:02d} · {s['status']} · {s['action']} {s.get('target','')}", "",
                  f"Expected: {s.get('expected') or s['action']}", f"Observed: {s.get('observed','')}", ""]
        if s.get("screenshot"):
            lines += [f"![Step {i}]({s['screenshot']})", ""]
    if run.get("error"):
        lines += ["## Run error", "", run["error"], ""]
    lines += ["## Reproduction", "", "Replay the frozen plan (fresh browser; same test data required):", "",
              "```sh", 'proofrunner replay <run-directory> --allow-interactions', "```", "",
              "Screenshots show observed state; root causes are not inferred from a failed assertion."]
    (directory / "report.md").write_text("\n".join(lines), encoding="utf-8")
    e = lambda x: html.escape(str(x), quote=True)
    cards = []
    for i,s in enumerate(run["steps"], 1):
        pic = f'<a href="{e(s["screenshot"])}"><img src="{e(s["screenshot"])}" alt="Evidence step {i}" loading="lazy"></a>' if s.get("screenshot") else ""
        cards.append(f'<section><div class="label">STEP {i:02d} · {e(s["status"])}</div><h2>{e(s["action"])} · {e(s.get("target",""))}</h2><p><b>Expected</b> {e(s.get("expected") or s["action"])}</p><p><b>Observed</b> {e(s.get("observed",""))}</p>{pic}</section>')
    doc = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'; base-uri 'none'">
<title>ProofRunner · {e(run['result'])}</title><style>
body{{background:#101721;color:#edf2f7;font:16px/1.6 system-ui;margin:auto;max-width:1040px;padding:48px 24px}}h1{{font-size:42px;line-height:1.15}}h2{{font-size:22px}}.label{{color:#93c5fd;letter-spacing:2px;font-size:12px;font-weight:700}}.status{{font-size:28px;color:{'#8ce8b5' if run['result']=='PASS' else '#ffac9d'}}}section{{background:#1b2533;border:1px solid #344257;border-radius:12px;padding:24px;margin:20px 0}}img{{max-width:100%;border-radius:6px;margin-top:16px}}b{{color:#93c5fd;margin-right:12px}}code{{overflow-wrap:anywhere}}a{{color:#93c5fd}}</style>
<div class="label">PROOFRUNNER / ACCEPTANCE EVIDENCE</div><h1>{e(run['name'])}</h1>
<div class="status">{e(run['result'])}</div><p><b>Target</b> {e(run['url'])}<br><b>Started</b> {e(run['started'])}<br><b>Duration</b> {run['duration']:.2f}s<br><b>Planner</b> {e(run['planner'])}</p>
{''.join(cards)}<section><h2>Reproduce this test</h2><code>proofrunner replay &lt;run-directory&gt; --allow-interactions</code><p>Fresh browser. Original assertions. Same test data required.</p><p>{e(run.get('error',''))}</p></section></html>'''
    (directory / "report.html").write_text(doc, encoding="utf-8")
