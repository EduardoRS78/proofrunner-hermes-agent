# Validation status — September 16, 2026

ProofRunner is a tested browser/evidence MVP with a live Hermes integration.
The repository is public, the agent is registered on the AI Worth Using Agent
Index, and the official client has successfully submitted measured model usage.
Manual organizer verification remains outstanding.

## Executed successfully

| Check | Actual result |
|---|---|
| Editable Python package installation | Succeeded on Linux / Python 3.12 |
| Core parser, strict schema, safety policy, redaction and report escaping | 13 tests passed |
| Real browser integration | 3 tests passed with Chromium |
| Official pinned Agent Index client self-check | Passed |
| Controlled CLI demo: login, cart count 1, total R$ 100,00 | PASS with seven screenshots |
| Deliberately broken demo: count stays 0 | FAIL at step 6; step 7 SKIPPED |
| Replay of the successful demo | PASS in a fresh browser/fixture |
| Windows smoke run | PASS on the user's Windows machine |
| Cloud release validation | Passed on GitHub Actions / Ubuntu |
| Live Hermes planner | Passed with `gemini-3.6-flash` |
| Agent Index registration | Registered as `proofrunner-eduardors78` |
| Official usage reporting | HTTP 200; 1,214 measured tokens submitted |
| Release evidence artifact | Uploaded by GitHub Actions |

The browser tests cover the successful journey, an intentional acceptance
failure with the original expectation preserved, and stopping an unauthorized
click. They use a real Chromium browser rather than DOM mocks. HTML and
execution JSON contain actual timestamps, locators, observed outcomes, and
step screenshots.

The live release workflow installs the pinned Hermes revision, runs
`proofrunner demo --planner hermes`, previews the official usage payload,
submits it through the official Agent Index client, confirms registered status,
and uploads the generated evidence. Secrets are stored only as protected GitHub
Actions secrets.

Agent page:
https://aiworthusing.com/agent-index/proofrunner-eduardors78

Successful release run:
https://github.com/EduardoRS78/proofrunner-hermes-agent/actions/runs/35150173135

## Still required or recommended

1. Request and pass the manual **Verified** organizer review.
2. Record a short public demo video and add its YouTube video ID to the listing.
3. Run a free-form journey against an authorized staging application.
4. Build and smoke-test the optional Docker image.
5. Keep the same registered install state when reporting future real usage;
   never reset identity or manufacture usage.

## Evidence included

- `examples/evidence/pass/`: successful controlled-English browser run.
- `examples/evidence/fail/`: deliberate acceptance failure.
- GitHub Actions artifact `proofrunner-agent-index-evidence`: live Hermes run.

The committed controlled examples are deliberately labeled as controlled rather
than Hermes-generated. Running the demos again creates new evidence under
`runs/` instead of modifying these reference runs.
