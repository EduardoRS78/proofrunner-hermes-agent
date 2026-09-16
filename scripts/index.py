"""Supervise the official client; never synthesize token usage or installation IDs."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import time
from fetch_index_client import main as install_client

ROOT = Path(__file__).resolve().parents[1]

def main():
    os.environ.setdefault("HERMES_HOME", str(ROOT / ".hermes"))
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["register", "report", "status", "self-check", "loop", "dry-run"])
    parser.add_argument("--repo", default="")
    args = parser.parse_args()
    install_client()
    command = [sys.executable, str(ROOT / "vendor/agent_index_client.py")]
    agent = os.environ.get("AGENT_ID", "proofrunner")
    def invoke(*flags):
        return subprocess.run([*command, *flags], check=False).returncode
    if args.mode == "self-check":
        return invoke("--self-check")
    if args.mode == "status":
        return invoke("status")
    if args.mode == "register":
        if not args.repo.startswith("https://github.com/"):
            parser.error("--repo must be the actual newly published public GitHub repository URL")
        return invoke("--register", "--agent", agent, "--name", "ProofRunner",
                      "--blurb", "AI-powered web acceptance agent that turns a natural-language journey into a real Chromium run with frozen assertions, step screenshots, and replayable PASS/FAIL evidence.",
                      "--runtime", "Hermes", "--repo", args.repo,
                      "--install-url", args.repo + "/blob/main/docs/installation.md",
                      "--image", args.repo + "/raw/main/examples/evidence/pass/screenshots/step-07.png",
                      "--image", args.repo + "/raw/main/examples/evidence/fail/screenshots/step-06.png")
    if args.mode == "dry-run":
        return invoke("--agent", agent, "--dry-run")
    if args.mode == "report":
        return invoke("--agent", agent)
    while True:
        state = invoke("status")
        if state == 3:
            state = invoke("--register", "--agent", agent)
        if state == 0:
            invoke("--agent", agent)
        else:
            print("Reporting paused: registration or stored-state error; see official client output", flush=True)
        time.sleep(300)

if __name__ == "__main__":
    raise SystemExit(main())
