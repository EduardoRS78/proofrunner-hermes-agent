"""Small, closed action language. Model output is data, never executable code."""
import json
import re
from dataclasses import asdict, dataclass

ACTIONS = {"navigate", "click", "fill", "fill_secret", "select", "wait", "read",
           "assert_text", "assert_url", "assert_visible", "assert_enabled", "assert_checked"}
ASSERTIONS = {x for x in ACTIONS if x.startswith("assert_")}

@dataclass
class Step:
    action: str
    target: str = ""
    value: str = ""
    expected: str = ""
    by: str = "auto"
    role: str = ""

    @classmethod
    def parse(cls, data):
        if not isinstance(data, dict) or set(data) - set(cls.__dataclass_fields__):
            raise ValueError("Invalid step fields")
        try:
            step = cls(**data)
        except TypeError as error:
            raise ValueError("Step action is required") from error
        if any(not isinstance(v, str) or len(v) > 4000 for v in asdict(step).values()):
            raise ValueError("Step fields must be short strings")
        if step.action not in ACTIONS or step.by not in {"auto", "label", "role", "text", "testid"}:
            raise ValueError("Unsupported action or locator")
        if step.action not in {"navigate", "assert_url"} and not step.target:
            raise ValueError("A target is required")
        if step.action == "navigate" and not step.value:
            raise ValueError("Navigation needs a URL")
        if step.action == "assert_text" and not step.expected:
            raise ValueError("Text assertion needs a nonempty expected value")
        if step.action == "assert_url" and not step.expected:
            raise ValueError("URL assertion needs an expected URL")
        if step.action == "fill_secret" and not re.fullmatch(r"PR_TEST_[A-Z0-9_]+", step.value):
            raise ValueError("Secrets must reference PR_TEST_* environment names")
        return step

def parse_plan(raw):
    if isinstance(raw, str):
        text = raw.strip()
        if text.startswith("```json") and text.endswith("```"):
            text = text[7:-3].strip()
        raw = json.loads(text)
    if not isinstance(raw, dict) or set(raw) != {"name", "steps"}:
        raise ValueError("Plan must contain only name and steps")
    if not isinstance(raw["name"], str) or not 1 <= len(raw["name"]) <= 160:
        raise ValueError("Invalid plan name")
    if not isinstance(raw["steps"], list) or not 1 <= len(raw["steps"]) <= 40:
        raise ValueError("Plan needs 1 to 40 steps")
    steps = [Step.parse(x) for x in raw["steps"]]
    if not any(s.action in ASSERTIONS for s in steps):
        raise ValueError("At least one explicit assertion is required; clicks alone cannot PASS")
    return {"name": raw["name"], "steps": [asdict(s) for s in steps]}
