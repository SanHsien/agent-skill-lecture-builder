[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

Write-Host "==> Run agent-skill-lecture-builder product verification suite (Windows)"

Write-Host "--> 1. Validate scripts syntax with Node.js"
$scripts = @(
    ".agents/skills/course-page-generator/scripts/build.mjs",
    ".agents/skills/course-page-generator/scripts/dev.mjs",
    ".agents/skills/course-page-generator/scripts/generate-og.mjs"
)
foreach ($s in $scripts) {
    node --check $s
    if ($LASTEXITCODE -ne 0) {
        throw "node --check $s failed with exit code $LASTEXITCODE"
    }
}

Write-Host "--> 2. Run course build on example directory"
$outputPath = Join-Path $repoRoot "example\index.html"
if (Test-Path -LiteralPath $outputPath) {
    Remove-Item -LiteralPath $outputPath -Force
}

node .agents/skills/course-page-generator/scripts/build.mjs example
if ($LASTEXITCODE -ne 0) {
    throw "build.mjs example failed with exit code $LASTEXITCODE"
}

Write-Host "--> 3. Validate generated index.html structure"
if (-not (Test-Path -LiteralPath $outputPath)) {
    throw "Output HTML file was not generated: $outputPath"
}

$fileSize = (Get-Item -LiteralPath $outputPath).Length
if ($fileSize -lt 5000) {
    throw "Generated HTML file is suspiciously small ($fileSize bytes)"
}

$htmlContent = Get-Content -LiteralPath $outputPath -Raw -Encoding utf8
$requiredMarkers = @(
    "<!DOCTYPE html>",
    "reveal",
    "section",
    "social-links"
)
foreach ($marker in $requiredMarkers) {
    if (-not $htmlContent.Contains($marker)) {
        throw "Generated HTML is missing expected marker: $marker"
    }
}

Write-Host "PRODUCT TESTS GREEN"
