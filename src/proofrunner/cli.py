import argparse
import json
import os
from pathlib import Path
from .demo import JOURNEY, demo_server
from .planner import HermesPlanner, controlled_plan
from .runner import execute
from .schema import parse_plan

def main():
    parser = argparse.ArgumentParser(description="Describe a journey. Run it. Get proof.")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="Real Chromium demo with controlled English; no LLM required")
    demo.add_argument("--broken", action="store_true")
    demo.add_argument("--planner", choices=["controlled", "hermes"], default="controlled")
    demo.add_argument("--output", default="runs")
    run = sub.add_parser("run", help="Run a natural-language journey")
    run.add_argument("url")
    run.add_argument("--journey", type=Path, required=True, help="UTF-8 text file")
    run.add_argument("--expect", default="")
    run.add_argument("--planner", choices=["hermes", "controlled"], default="hermes")
    run.add_argument("--allow-interactions", action="store_true", help="Authorize interactions on this test origin")
    run.add_argument("--output", default="runs")
    replay = sub.add_parser("replay", help="Replay recorded plan without a model")
    replay.add_argument("directory", type=Path)
    replay.add_argument("--allow-interactions", action="store_true")
    replay.add_argument("--output", default="runs")
    args = parser.parse_args()
    planner = None
    try:
        if getattr(args, "planner", None) == "hermes":
            planner = HermesPlanner()
        if args.command == "demo":
            # A synthetic fixture credential, scoped to this process and restored.
            old = os.environ.get("PR_TEST_PASSWORD")
            os.environ["PR_TEST_PASSWORD"] = "demo-pass"
            try:
                with demo_server() as url:
                    url += "?broken=1" if args.broken else ""
                    plan = planner.plan(url, JOURNEY, "Cart count must equal 1 and total R$ 100,00") if planner else controlled_plan(JOURNEY)
                    directory, result = execute(url, plan, prompt=JOURNEY, planner=planner,
                        planner_name=args.planner, output=args.output, interactions=True, local_demo=True)
                    result["demo_broken"] = args.broken
                    from .report import write_reports
                    write_reports(directory, result)
            finally:
                if old is None:
                    os.environ.pop("PR_TEST_PASSWORD", None)
                else:
                    os.environ["PR_TEST_PASSWORD"] = old
        elif args.command == "run":
            journey = args.journey.read_text(encoding="utf-8")
            plan = planner.plan(args.url, journey, args.expect) if planner else controlled_plan(journey, args.expect)
            directory, result = execute(args.url, plan, prompt=journey, planner=planner,
                planner_name=args.planner, output=args.output, interactions=args.allow_interactions)
        else:
            previous = json.loads((args.directory / "execution.json").read_text(encoding="utf-8"))
            plan = parse_plan(previous["plan"])
            if previous.get("local_demo"):
                old = os.environ.get("PR_TEST_PASSWORD")
                os.environ["PR_TEST_PASSWORD"] = "demo-pass"
                try:
                    with demo_server() as url:
                        url += "?broken=1" if previous.get("demo_broken") else ""
                        directory, result = execute(url, plan, planner_name="replay", output=args.output,
                                                   interactions=args.allow_interactions, local_demo=True)
                        result["demo_broken"] = previous.get("demo_broken", False)
                        from .report import write_reports
                        write_reports(directory, result)
                finally:
                    if old is None:
                        os.environ.pop("PR_TEST_PASSWORD", None)
                    else:
                        os.environ["PR_TEST_PASSWORD"] = old
            else:
                directory, result = execute(previous["url"], plan, planner_name="replay", output=args.output,
                                           interactions=args.allow_interactions)
        print(f"{result['result']} | {directory.resolve() / 'report.html'}")
        return {"PASS":0, "FAIL":1, "ERROR":2}[result["result"]]
    except (ValueError, RuntimeError, OSError, KeyError) as error:
        print(f"ERROR: {type(error).__name__}: {error}")
        return 2
    finally:
        if planner:
            planner.close()

if __name__ == "__main__":
    raise SystemExit(main())
