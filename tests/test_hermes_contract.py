"""Actual Hermes SDK against a LOCAL deterministic provider stub.

This validates the adapter contract, not real model reasoning or paid inference.
Never register/report this temporary test home to the Agent Index.
"""
import json
import pytest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from proofrunner.demo import JOURNEY
from proofrunner.planner import HermesPlanner, controlled_plan

def test_real_hermes_sdk_with_local_provider(tmp_path, monkeypatch):
    pytest.importorskip("run_agent", reason="Optional Hermes SDK contract test requires upstream Hermes")
    plan = controlled_plan(JOURNEY)
    requests = []
    class Provider(BaseHTTPRequestHandler):
        def do_POST(self):
            request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            requests.append(request)
            response = {"id":"local-contract-test", "object":"chat.completion", "created":0,
                "model":"proofrunner-contract-test", "choices":[{"index":0,"message":{"role":"assistant",
                "content":json.dumps(plan)}, "finish_reason":"stop"}],
                "usage":{"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}}
            if request.get("stream"):
                response["object"] = "chat.completion.chunk"
                response["choices"][0]["delta"] = response["choices"][0].pop("message")
                body = ("data: " + json.dumps(response) + "\n\ndata: [DONE]\n\n").encode()
            else:
                body = json.dumps(response).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream" if request.get("stream") else "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", 0), Provider)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "isolated-hermes"))
    monkeypatch.setenv("PROOFRUNNER_BASE_URL", f"http://127.0.0.1:{server.server_port}/v1")
    monkeypatch.setenv("PROOFRUNNER_API_KEY", "local-placeholder-not-a-real-key")
    monkeypatch.setenv("PROOFRUNNER_MODEL", "proofrunner-contract-test")
    planner = None
    try:
        planner = HermesPlanner()
        assert not planner.agent.tools
        actual = planner.plan("https://example.com", JOURNEY, "Count equals 1")
        assert actual == plan
        assert requests and not requests[0].get("tools")
    finally:
        if planner:
            planner.close()
        server.shutdown()
        server.server_close()
        thread.join()
