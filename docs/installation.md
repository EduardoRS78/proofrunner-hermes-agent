# Installation

## Browser executor and repeatable local demo

Extract the project or clone its actual published repository, then open a
terminal in its root. Python 3.11–3.13 is recommended for compatibility with
Hermes. Native Python/Playwright works on Windows, Linux and macOS.

```sh
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` in Windows PowerShell, or
`source .venv/bin/activate` on Linux/macOS. Then:

```sh
python -m pip install -e ".[test]"
python -m playwright install chromium
proofrunner demo
```

On Linux, a minimal system may need `python -m playwright install --with-deps
chromium`. Installation time depends on the browser download.

## Free-form natural language through Hermes

ProofRunner embeds the official `run_agent.AIAgent`. Install the inspected
upstream revision **in the same Python environment**:

```sh
git clone https://github.com/NousResearch/hermes-agent.git ../hermes-agent
git -C ../hermes-agent checkout 10652c93451fb760435d39d1ce4fd8a9441d18b9
python -m pip install -e ../hermes-agent
# Linux/macOS: export HERMES_HOME="$PWD/.hermes"
# PowerShell: $env:HERMES_HOME = Join-Path $PWD '.hermes'
hermes model
proofrunner demo --planner hermes
```

`hermes model` configures your inference provider interactively. Alternatively
set `PROOFRUNNER_MODEL`, `PROOFRUNNER_BASE_URL`, and `PROOFRUNNER_API_KEY` for a
provider endpoint you control. Do not assume a ChatGPT subscription supplies
API credit. This adapter uses the Hermes SDK and its real session store.

For the hackathon, set `HERMES_HOME` to a **dedicated ProofRunner home** before
configuring Hermes. Do not point reporting at unrelated personal sessions.

PowerShell example:

```powershell
$env:HERMES_HOME = Join-Path $PWD '.hermes'
$env:PR_TEST_USER = 'your-test-user'
$env:PR_TEST_PASSWORD = Read-Host 'Test password' -MaskInput
proofrunner run 'https://your-staging-site.example' --journey examples/journey.txt --allow-interactions
```

`Read-Host -MaskInput` requires PowerShell 7.1+. In older PowerShell, use your
secret manager or a temporary process environment; do not type a real secret
into command history. Native CLI does not automatically load `.env`.

## Docker Desktop on Windows / Docker Engine on Linux

```powershell
Copy-Item .env.example .env
# Set your provider variables in .env locally, then:
docker compose build
docker compose run --rm proofrunner demo
docker compose run --rm proofrunner demo --planner hermes
```

Linux/macOS: use `cp .env.example .env`. The Docker image includes upstream
Hermes, Playwright, Chromium and the verified official reporter. It runs as a
non-root user. The first image build can take longer than five minutes.

`runs/` contains evidence. `hermes-data` preserves sessions and the official
reporter's install identity. Keep this named volume when recreating containers.
Do not run `docker compose down -v` to troubleshoot: it deletes that identity.

The image does not use Plow Chat, so a phone line is not required for browser
execution. Agent Index registration still needs an official Plow credential.
Obtaining it without an Apple device may require organizer assistance; the
kickoff allowed the non-Mac route, but the current credential CLI documents a
text-message activation flow. See docs/agent-index.md.
