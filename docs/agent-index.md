# Official Agent Index integration

Official sources:
- https://github.com/plow-pbc/agent-index-client
- https://github.com/plow-pbc/plow-agents
- https://aiworthusing.com/agent-index

The project downloads `standalone/agent_index_client.py` at revision
`87901f8b182a8a7c65ee3dd7267f8f835ee2a545`, with SHA-256
`c3bf54ed37aec22704b8003a7ff6385a1fd3ef49207ce55613ddc41df36a1b01`.
The pin and digest came from the official life-assistant image's client.pin.
The fetched file is not committed or relicensed as project code.

The client supports `--register`, `status`, `--agent`, `--dry-run`, and
`--self-check`. It reads actual Hermes `state.db` usage and reports day/model
token counts, not prompts, screenshots, or journey text. A registration also
publishes the supplied listing metadata. Never create fake use or reset
install identity to inflate installations.

## Obtain credentials

The official plow-agents flow is:

```sh
git clone https://github.com/plow-pbc/plow-agents.git
# Run these from the ProofRunner checkout, using the actual CLI path:
../plow-agents/bin/plow-agents login
../plow-agents/bin/plow-agents lines
../plow-agents/bin/plow-agents mint <free-line-id>
```

The CLI is Python; on Windows, use it from WSL with
`python3 ../plow-agents/bin/plow-agents ...`. SMS activation and credential
minting were successfully completed from WSL on Windows. Keep the minted
credentials local and out of Git; GitHub Actions receives only the protected
`PLOW_AGENT_TOKEN` repository secret.

## Publish and report

Set `PLOW_AGENT_TOKEN` from the officially issued credential, `AGENT_ID` to
your chosen available id, and `HERMES_HOME` to the dedicated ProofRunner home.
The default `proofrunner` ID is a suggestion; availability is not confirmed.

```sh
python scripts/index.py self-check
python scripts/index.py register --repo https://github.com/<owner>/<new-repository>
proofrunner demo --planner hermes
python scripts/index.py dry-run
python scripts/index.py report
```

Replace the repository placeholder with the real public URL. Register **before**
collecting demo usage when possible; the official collector establishes a
baseline. Controlled/replay runs do not invoke a model and must not be
reported as model token consumption.

In Docker, `.env` supplies the credential and the named volume keeps the same
Hermes home across runs:

```sh
docker compose run --rm --entrypoint python proofrunner scripts/index.py register --repo https://github.com/<owner>/<new-repository>
docker compose run --rm proofrunner demo --planner hermes
docker compose --profile index up -d reporter
docker compose logs reporter
```

The supervised loop runs every five minutes. `status=3` means register first;
unreadable state is not treated as unregistered. Failures remain visible in
the official client's output. A missing explicitly configured Hermes store
is a collector error, not zero usage. Keep the named volume to retain install
identity. Do not aim this reporter at your general-purpose Hermes sessions.

## Verified is manual

After publishing, open the agent page and click **Get my agent verified**.
The Index says hosts install/run agents, safety verification is required to
win, and verification begins September 14, 2026. A successful API registration
does not make an agent Verified. One-click Plow hosting is coordinated with
the Plow team; it is not required for the local executor to run.

ProofRunner was registered as `proofrunner-eduardors78` on September 16,
2026. The release workflow completed a real Hermes run with
`gemini-3.6-flash`, submitted 1,214 measured tokens through the official
client, confirmed registered status, and uploaded the generated evidence.
Manual organizer verification remains outstanding. See validation.md for exact
test coverage.
