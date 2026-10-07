[CmdletBinding()]
param(
    [switch]$All
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "==> Check Node & Python"
node -v
python -c "import sys; print(sys.version)"

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Host "==> Create .venv"
    python -m venv .venv
}

Write-Host "==> Install maintenance dependencies"
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "pip upgrade failed with exit code $LASTEXITCODE"
}
& $venvPython -m pip install -r (Join-Path $repoRoot "requirements-dev.txt")
if ($LASTEXITCODE -ne 0) {
    throw "pip install requirements-dev.txt failed with exit code $LASTEXITCODE"
}

if ($All) {
    Write-Host "==> Install optional dev dependencies (npm install)"
    npm install
    if ($LASTEXITCODE -ne 0) {
        throw "npm install failed with exit code $LASTEXITCODE"
    }
}

Write-Host "==> Canonical Windows gate"
& pwsh -NoProfile -File (Join-Path $repoRoot "tools\dev_check.ps1")

Write-Host "==> Product tests"
& pwsh -NoProfile -File (Join-Path $repoRoot "tools\test_product.ps1")

Write-Host ""
Write-Host "維護環境可用。要使用課程頁建置工具與 Skill 請參考 docs\DEVELOPMENT.md"
