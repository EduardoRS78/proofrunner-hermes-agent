# Architecture and boundaries

`schema.py` defines a finite action language. No arbitrary code, shell, CSS,
XPath, or model-supplied JavaScript is executed. `planner.py` uses Hermes
`AIAgent` without tools and refuses to start if tools unexpectedly load.
Hermes records provider-reported usage in its own SessionDB; ProofRunner
never writes token counts into that database itself.

The plan is frozen before browser actions. At each step the executor resolves
accessible labels, roles, test IDs or exact text. If those do not resolve,
Hermes may identify a locator from a redacted accessibility snapshot; this
cannot alter the action or acceptance expectation. Duplicate matches are not
resolved by choosing the first one.

`runner.py` executes in a fresh context, captures an image after every
executed step and on failures, records resolved locators, and stops at the
first failed/error step. All following steps are SKIPPED. A run without an
explicit assertion is invalid. Missing screenshot evidence turns a step into
ERROR. Report writes occur after each step and at termination.

Text equality uses Playwright's whitespace-normalized exact assertion, not
substring matching. URL assertions use the full exact supplied string.
An assertion mismatch is FAIL; blocked actions, missing secrets, invalid
planner output and setup failures are ERROR. Action completion does not imply
the subsequent acceptance criterion passed.

## Safety model

Read-only mode blocks interactions and non-GET/HEAD/OPTIONS requests.
`--allow-interactions` authorizes writes on the supplied staging origin only.
All resource requests, not just top-level navigations, are origin checked.
Private addresses, metadata IPs, WebSockets, service workers, popups, dialogs
and downloads are blocked. Only the built-in fixture gets a loopback exception.
The browser has no shared user profile or real account cookies.

Conservative action/endpoint checks stop obvious purchases, payments,
deletion and messages. They are heuristic, not proof that a website's backend
is safe. GET endpoints can mutate state; same-origin pages can conceal side
effects; DNS checks are not a substitute for a network firewall and are
subject to DNS changes between resolution and connection. Do not execute
untrusted websites or production transactions. Use disposable staging data.

Screenshot masking covers form inputs and DOM text containing known test
secrets. It cannot detect every kind of private data, canvas rendering, or
image-embedded information. Reports may contain other staging data. Review
before sharing. Do not put secrets in URLs or journey text. Query/fragment
components are stripped from recorded URLs, so replay does not preserve an
external query-dependent initial state in this MVP.

No email inbox connector is included. Password recovery with a mailed link,
CAPTCHA, MFA, external SSO, iframes, multi-tab and cross-origin CDNs are outside
the MVP. Replay repeats a frozen plan; it does not restore server-side state.

## Why not start from the Plow cloud base?

The current plow-hermes-agent README explicitly says there is no local mode
and the base boots through Plow Chat identity provisioning. For this user's
Windows/non-iPhone route, the smaller dependency is upstream Hermes embedded
directly, plus the required official reporting client. This follows the
kickoff's alternative route and the current Luma list, which encourages
Latch/phone integration but requires the Index client. The image is a complete
CLI agent, browser executor and evidence pipeline, not a skill-only entry.

Inspect the current rules with organizers before submission. No claim of
Verified status or eligibility is made by this architectural choice.
