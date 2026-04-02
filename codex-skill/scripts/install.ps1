$ErrorActionPreference = "Stop"

param(
    [switch]$Force,
    [switch]$Verify,
    [switch]$Sync,
    [string]$DestRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillDir = Split-Path -Parent $scriptDir

if ($DestRoot) {
    $destRoot = $DestRoot
} else {
    $codexHome = if ($env:CODEX_HOME) {
        $env:CODEX_HOME
    } elseif ($env:USERPROFILE) {
        Join-Path $env:USERPROFILE ".codex"
    } else {
        throw "CODEX_HOME is not set and USERPROFILE is unavailable."
    }
    $destRoot = Join-Path $codexHome "skills"
}

$destDir = Join-Path $destRoot "cli-anything"

function Resolve-Python {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return "python"
    }
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return "py -3"
    }
    throw "Python is required to install or verify the Codex skill."
}

$pythonCmd = Resolve-Python

if ($Sync) {
    Invoke-Expression "$pythonCmd `"$scriptDir\sync_from_plugin.py`""
}

New-Item -ItemType Directory -Path $destRoot -Force | Out-Null

if (Test-Path $destDir) {
    if (-not $Force) {
        throw "Refusing to overwrite existing skill: $destDir`nRe-run with -Force to replace it."
    }
    Remove-Item -Path $destDir -Recurse -Force
}

Copy-Item -Path $skillDir -Destination $destDir -Recurse

if ($Verify) {
    Invoke-Expression "$pythonCmd `"$scriptDir\verify_install.py`" `"$destDir`""
}

Write-Host "Installed Codex skill to: $destDir"
Write-Host "Restart Codex to pick up the new skill."
