# Troubleshooting

**Executable does not exist / Chromium missing:** run `python -m playwright
install chromium` in the same environment. A network timeout means the browser
was not installed. Do not interpret the resulting ERROR report as a site failure.

**Linux shared libraries missing:** `python -m playwright install --with-deps
chromium`, or use the Docker image. This may require your system administrator.

If your environment already provides a compatible Chromium executable, set
`PROOFRUNNER_BROWSER_EXECUTABLE` to its absolute path. This is an optional
host configuration, never a value the page/model can supply. The standard
installation uses Playwright's own browser. The build-environment browser
verification used Chromium 153 from @sparticuz/chromium after the normal CDN
download timed out; this fallback is not a dependency shipped in the project.

**Hermes is not installed:** activate the same venv and follow installation.md.
Installing an unrelated PyPI package named Hermes is not the supported route.

**Provider authentication/model error:** configure `hermes model`, or the
documented PROOFRUNNER variables. Never send your key in a chat or commit it.

**No unique visible element:** specify an accessible name, use a stable
test-id, or run with the Hermes planner. Duplicate matches fail deliberately.
Add an explicit wait step with a known locator for asynchronous page content.

**Safety/origin error:** use a staging flow confined to one origin. Third-party
login, external scripts/CDNs, iframes and real checkout are outside the MVP.
There is no general-purpose override to run an arbitrary destructive action.

**Docker report directory permission:** ensure the mounted runs directory is
writable by UID 10001. On Linux, a directory you create may need ownership
adjustment. Do not run the agent privileged to solve a filesystem permission.

**Index says configured but missing:** HERMES_HOME must hold a real Hermes
state.db. Run a successful Hermes journey first; never fabricate a database
or token rows. Run official `self-check` and `dry-run`, inspect errors.

**Missing reports for a failed planning step:** no browser was started because
the plan/provider failed. The CLI prints ERROR with exit 2. Browser execution
errors do produce reports, including initial navigation failures.

**Only controlled-English demo works:** browser execution is available but
the general natural-language feature is not yet validated. This is not a
complete hackathon release until a real Hermes/provider run succeeds.
