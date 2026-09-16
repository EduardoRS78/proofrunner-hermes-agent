# Research and submission gates — checked September 16, 2026

## Primary sources

The complete supplied kickoff transcription was read. Relevant timestamps:
09:36–12:50 (real usage, Top 10, human review), 18:05–19:14 (three integration
routes, including non-Mac/non-iPhone), 26:58 (Tiago's QA bot), 31:54–35:05
(base image, credentials, reporting), 37:20 (working open-source agent, not
just a skill). The transcript is machine-generated and may contain errors.

- Official event: https://luma.com/3uftu95w
- Official index: https://aiworthusing.com/agent-index
- Runtime: https://github.com/NousResearch/hermes-agent
- Plow base: https://github.com/plow-pbc/plow-hermes-agent
- Credentials: https://github.com/plow-pbc/plow-agents
- Reporting: https://github.com/plow-pbc/agent-index-client
- Working official variant: https://github.com/plow-pbc/life-assistant-hermes-agent

## Confirmed current text

The current event text requires MIT, publicly available code, an installable
agent through the Agent Index, Verified status and official usage reporting.
It lists September 16 as submission deadline, without a cutoff time in the
retrieved text. It gives September 23 at 1pm PT as the leaderboard snapshot.
Plow Latch and the phone plugin are encouraged products; the Index client is
required. No required repository naming convention was found. A new public
GitHub repository with an MIT license is consistent with these requirements.

The Agent Index describes Verified as installed/run by hosts and safety
verification as necessary to win. It provides a manual verification button.

## Conflict / do not silently resolve

The kickoff explicitly changed selection to Top 10 followed by human review.
The currently retrieved Luma text instead states first/second ranked at the
snapshot win. We cannot establish whether the page or meeting takes
precedence. Ask organizers before relying on either judging scheme. Also
confirm today's submission cutoff/timezone and the non-iPhone credential
issuance route. No message was sent on the user's behalf.

## Competitor comparison

Repository READMEs inspected:

| Project | Main purpose | Overlap / lesson |
|---|---|---|
| [Oncall Solo](https://github.com/gabe-rbo/oncall-solo-hermes-agent) | HTTP/TCP/CI incident monitoring and diagnosis | Closest evidence/diagnosis overlap; not user-journey acceptance. Clear installation and conservative action authorization. |
| [Video Cuts](https://github.com/gilvanecesar/video-cuts) | Recording-to-published-clips pipeline | Clear end-to-end output and memorable demo; different problem. |
| [Transcritor](https://github.com/eudanielhenrique/transcritor) | Multimodal transcription and content synthesis | Packaged Plow runtime; different problem. |
| [TISS Guard](https://github.com/joaomargalho/tiss-guard) | Healthcare XML validation and correction | Explicit deterministic checks and before/after reporting; not browser QA. |
| [Saved](https://github.com/AElise08/saved-hermes-agent) | Personal capture vault and weekly ideas | Onboarding simplicity and installation documentation; different problem. |

Oncall Solo declares Apache-2.0 while Luma requires MIT. A competitor's choice
does not override the official rule; ProofRunner code uses MIT. Dependencies
keep their own licenses. No competitor code was copied.

The five supplied screenshots cover ranks 1–40 with one overlapping row.
They show infrastructure monitoring, financial tools, scheduling, media,
computer control and other agents; they do not establish a duplicate of the
complete proposed evidence/replay workflow. Tiago's kickoff QA bot and the
Founder Agent listing remain relevant overlaps.

The live web extraction returned the Index shell with 'Loading' rather than
the complete current competitor table. Searches did not establish an exhaustive
current list. Therefore **absence of an identical competitor is not proven**.
No pivot is justified by the evidence available so far.

## Differentiation to demonstrate

Explicit acceptance contract, fixed expected values, real Playwright checks,
PASS and deliberately broken FAIL cases, evidence per step, frozen locator
record and replay without additional inference. This is a practical distinction
from generic computer-control bots and incident monitors, not a claim that
natural-language QA is globally novel.

## Release gates

- Successful real browser run and deliberate assertion failure.
- Successful free-form Hermes/provider run with stored real token usage.
- Docker build and Windows installation smoke test.
- New public GitHub repository with MIT and no secrets.
- Official Agent Index registration/report accepted with real credentials.
- Organizer safety verification; resolve judging/deadline ambiguity.

See validation.md for achieved vs pending gates. Do not advertise submission
readiness or Verified status until these gates are actually satisfied.
