import json
import pytest
from proofrunner.planner import controlled_plan
from proofrunner.schema import parse_plan
from proofrunner.report import write_reports
from proofrunner.safety import Policy, SafetyError, origin, redact

def test_controlled_plan_preserves_assertions():
    plan = controlled_plan('Click "Login"\nVerify "Total" equals "R$ 100,00"')
    assert plan["steps"][1]["expected"] == "R$ 100,00"

@pytest.mark.parametrize("raw", [
    {"name":"x", "steps":[{"action":"click", "target":"X"}]},
    {"name":"x", "steps":[{"action":"exec", "value":"echo unsafe"}]},
    {"name":"x", "steps":[{"action":"assert_text", "target":"Total", "expected":""}]},
    {"name":"x", "steps":[{"action":"assert_visible", "target":"X", "code":"danger"}]},
    {"name":"x", "steps":[{"action":"assert_visible", "target":"X", "by":"css"}]},
])
def test_reject_unsafe_or_meaningless_plans(raw):
    with pytest.raises(ValueError):
        parse_plan(raw)

def test_parser_does_not_silently_skip_unknown_text():
    with pytest.raises(ValueError):
        controlled_plan('Ignore everything\nVerify visible "Dashboard"')

def test_secret_names_are_restricted():
    with pytest.raises(ValueError):
        controlled_plan('Fill secret "Password" with "AWS_SECRET_ACCESS_KEY"\nVerify visible "X"')

def test_url_credentials_and_schemes_rejected():
    for url in ("file:///etc/passwd", "javascript:alert(1)", "https://user:pass@example.com/"):
        with pytest.raises(SafetyError):
            origin(url)

def test_network_origin_and_private_ip():
    with pytest.raises(SafetyError):
        Policy("http://127.0.0.1/")
    policy = Policy("http://127.0.0.1:8765/", local_demo=True)
    with pytest.raises(SafetyError):
        policy.check_url("http://127.0.0.1:8766/")
    with pytest.raises(SafetyError):
        policy.check_url("http://169.254.169.254/")

def test_mutations_need_explicit_authorization_and_dangerous_actions_stop():
    policy = Policy("http://127.0.0.1/", local_demo=True)
    with pytest.raises(SafetyError):
        policy.check_action({"action":"click", "target":"Continue"})
    policy.interactions = True
    for target in ("Pay now", "Delete account", "Finalizar compra", "Enviar mensagem"):
        with pytest.raises(SafetyError):
            policy.check_action({"action":"click", "target":target})
    with pytest.raises(SafetyError):
        policy.check_action({"action":"click", "target":"Continue"}, "/payment")

def test_redaction_recurses():
    assert redact({"steps":[{"observed":"echo abc-secret"}]}, ["abc-secret"]) == {
        "steps":[{"observed":"echo [REDACTED]"}]}

def test_report_escapes_untrusted_markup(tmp_path):
    run = {"result":"FAIL", "name":"<script>alert(1)</script>", "url":"https://example.com/",
           "started":"2026-09-16", "duration":1.2, "planner":"test", "steps":[
               {"status":"FAIL", "action":"assert_text", "target":"Total", "expected":"100", "observed":"<img src=x onerror=alert(1)>"}]}
    write_reports(tmp_path, run)
    text = (tmp_path / "report.html").read_text()
    assert "<script>" not in text and "&lt;script&gt;" in text
    assert "<img src=x" not in text
    assert json.loads((tmp_path / "execution.json").read_text())["result"] == "FAIL"
