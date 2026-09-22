[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

Set-Location $ProjectRoot

if (-not (Test-Path $VenvPython)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        Write-Host "Creating Python 3.12 environment..."
        & py -3.12 -m venv .venv
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        Write-Host "Creating Python environment..."
        & python -m venv .venv
    }
    else {
        throw "Python was not found. Install Python 3.11, 3.12, or 3.13 and run this script again."
    }
}

Write-Host "Installing ProofRunner..."
& $VenvPython -m pip install -e .
if ($LASTEXITCODE -ne 0) { throw "ProofRunner installation failed." }

Write-Host "Installing Chromium..."
& $VenvPython -m playwright install chromium
if ($LASTEXITCODE -ne 0) { throw "Chromium installation failed." }

Write-Host ""
Write-Host "ProofRunner is ready." -ForegroundColor Green
Write-Host 'Try: .\run.ps1 -Url "https://example.com/"'
