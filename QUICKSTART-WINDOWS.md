# ProofRunner quick start for Windows

Requirements: Git and Python 3.11-3.13.

Open PowerShell in the repository and allow scripts for this terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Install ProofRunner and Chromium once:

```powershell
.\setup.ps1
```

Run the included read-only test against a real public website:

```powershell
.\run.ps1 -Url "https://example.com/"
```

The report is written under `runs\<run-id>\report.html`.

To test another authorized website, create a UTF-8 journey file and provide it:

```powershell
.\run.ps1 -Url "https://your-authorized-site.example/" -JourneyFile ".\my-journey.txt"
```

For free-form instructions, configure Hermes and an LLM provider, then use:

```powershell
.\run.ps1 -Url "https://your-authorized-site.example/" -JourneyFile ".\my-journey.txt" -Planner hermes
```

Use `-AllowInteractions` only when you explicitly authorize clicks and form input on that test origin. Never authorize real purchases, payments, messages, account deletion, or other destructive actions.
