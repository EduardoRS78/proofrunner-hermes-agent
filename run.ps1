[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^https://')]
    [string]$Url,

    [string]$JourneyFile = "examples/public-site-journey.txt",

    [ValidateSet("controlled", "hermes")]
    [string]$Planner = "controlled",

    [switch]$AllowInteractions
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$Runner = Join-Path $ProjectRoot ".venv\Scripts\proofrunner.exe"

if (-not (Test-Path $Runner)) {
    throw "ProofRunner is not installed. Run .\setup.ps1 first."
}

if (-not [System.IO.Path]::IsPathRooted($JourneyFile)) {
    $JourneyFile = Join-Path $ProjectRoot $JourneyFile
}

if (-not (Test-Path $JourneyFile)) {
    throw "Journey file not found: $JourneyFile"
}

$Arguments = @(
    "run",
    $Url,
    "--journey", (Resolve-Path $JourneyFile).Path,
    "--planner", $Planner,
    "--output", (Join-Path $ProjectRoot "runs")
)

if ($AllowInteractions) {
    $Arguments += "--allow-interactions"
}

& $Runner @Arguments
exit $LASTEXITCODE
