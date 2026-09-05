<#
.SYNOPSIS
    Project Ebony: Sovereign Command Center Orchestrator (Public Blueprint)
    Spawns Ingress Daemon, launches Pear Desktop UI, and streams continuous Protocol Lambda V2 telemetry.
    Author: Jeffery Humphrey, CEO & Apex Architect
#>

$ErrorActionPreference = "Stop"
$PEAR_LINK = "pear://<PROJECT_LINK_REDACTED>"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " PROJECT EBONY: SOVEREIGN COMMAND CENTER LAUNCHER (PUBLIC)" -ForegroundColor Cyan
Write-Host " Status: Iron Dome Compliant" -ForegroundColor Green
Write-Host " Target Link: $PEAR_LINK" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan

# 1. Start Ingress Diode Daemon in separate background process
Write-Host "[1/3] Activating Ingress Diode Daemon (UDP 127.0.0.1:5005)..." -ForegroundColor Green
$daemonProc = Start-Process -FilePath "cmd.exe" -ArgumentList "/c node bridge_daemon.js" -WorkingDirectory (Get-Location).Path -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 2

# 2. Launch Pear Desktop Command Center Window
Write-Host "[2/3] Launching Pear Desktop Command Center..." -ForegroundColor Green
Start-Process -FilePath "cmd.exe" -ArgumentList "/c pear run $PEAR_LINK" -WorkingDirectory (Get-Location).Path
Start-Sleep -Seconds 4

# 3. Launch Continuous Telemetry Emitter via CMD Environment Resolver
Write-Host "[3/3] Starting Continuous Telemetry Stream (Protocol Lambda V2)..." -ForegroundColor Green
Write-Host "`nYour Command Center window is running live." -ForegroundColor Yellow
Write-Host "Observe live telemetry updating on screen. Press Ctrl+C when finished." -ForegroundColor Cyan

try {
    cmd.exe /c "node stream_continuous.js"
}
finally {
    Write-Host "`n[TEARDOWN] Terminating Ingress Diode Daemon..." -ForegroundColor Yellow
    Stop-Process -Id $daemonProc.Id -Force -ErrorAction SilentlyContinue
    Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*bridge_daemon.js*" } | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "[TEARDOWN] Command Center session closed cleanly." -ForegroundColor Green
}
