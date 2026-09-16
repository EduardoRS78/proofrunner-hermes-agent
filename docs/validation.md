# Validation status — September 16, 2026

This is a tested browser/evidence MVP with a Hermes adapter. It is **not yet
a fully validated hackathon release**. No real inference credential was
available, no public repository was created, and no Agent Index registration
or verification request was submitted.

## Executed successfully

| Check | Actual result |
|---|---|
| Editable Python package installation | Succeeded on Linux / Python 3.12 |
| Core parser, strict schema, safety policy, redaction and report escaping | 13 tests passed |
| Real browser integration | 3 tests passed |
| Real Hermes SDK with local deterministic provider stub | 1 test passed; not real model reasoning |
| Official pinned Agent Index client self-check | Passed |
| CLI demo: login, cart count 1, total R$ 100,00 | PASS, seven screenshots |
| CLI broken demo: count stays 0 | FAIL at step 6; step 7 SKIPPED |
| Replay of the successful demo | PASS in a fresh browser/fixture |
| Visual inspection | Final store screenshot and rendered HTML report checked |

The browser tests cover the successful journey, an intentional acceptance
failure with unchanged expected value, and stopping an unauthorized click.
They use a real Chromium browser, not DOM mocks. HTML and execution JSON
include actual timestamps, locators and observed outcomes.

The standard Playwright browser download timed out in this environment.
Validation used Playwright Python 1.63.0 with Chromium 153.0.8010.0 supplied
by `@sparticuz/chromium` 153.0.0 and the explicit executable-path setting.
That temporary binary is not included in the repository or deliverable.

Hermes at commit `10652c93451fb760435d39d1ce4fd8a9441d18b9` was installed and
imported successfully. The adapter contract test exercised its real streaming
inference client against a local test server returning a known plan. This
isolated test home has zero reported tokens and was never registered with
the Index. It does not validate natural-language reasoning, paid provider
authentication, or live usage reporting.

## Still required

1. Configure a real inference provider and run `proofrunner demo --planner
   hermes`, followed by a free-form journey on an authorized staging site.
2. Build the Docker image (Docker is not installed in the build environment).
3. Run the Windows installation smoke test on the user's machine.
4. Create the new public GitHub repository, then push the tested commits.
5. Obtain an official Plow credential, register and send a real usage report.
6. Request manual Verified review and confirm deadline/judging ambiguities.

The connected GitHub tools expose file/commit operations and authenticated
profile access, but no new-repository creation operation. Publication needs
the user to create the new repository first or provide a supported creation
capability. No existing user repository was changed.

## Evidence included

- `examples/evidence/pass/`: actual successful controlled-English run.
- `examples/evidence/fail/`: actual broken controlled-English run.

These examples are deliberately labeled controlled, not Hermes-generated.
Open `report.html` beside its screenshot folder. Running the demos again
creates new evidence under `runs/` instead of modifying these reference runs.
