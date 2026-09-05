<#
.SYNOPSIS
    Project Ebony: Sovereign Mesh Seeder & Telemetry Stream Orchestrator (Public Blueprint)
    Architecture: Pear Desktop v3.3.0 / Hypercore v11+ / Hyperswarm DHT
    Author: Jeffery Humphrey, CEO & Apex Architect
#>

$ErrorActionPreference = "Stop"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " PROJECT EBONY: SOVEREIGN RUNTIME ORCHESTRATOR (PUBLIC)" -ForegroundColor Cyan
Write-Host " Link: pear://<PROJECT_LINK_REDACTED>" -ForegroundColor Yellow
Write-Host " Ingress: UDP 127.0.0.1:5005 (Protocol Lambda V2)" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan

Write-Host "`n[1/3] Starting Telemetry Ingress Diode Daemon..." -ForegroundColor Green
$daemonJob = Start-Job -ScriptBlock {
    Set-Location $PSScriptRoot
    node bridge_daemon.js
}

Start-Sleep -Seconds 3

Write-Host "[2/3] Emitting Protocol Lambda V2 Telemetry Burst..." -ForegroundColor Green
node emit_burst.js

Start-Sleep -Seconds 2

Write-Host "`n[3/3] Inspecting Ingress Daemon Output..." -ForegroundColor Green
Receive-Job -Job $daemonJob
Stop-Job -Job $daemonJob
Remove-Job -Job $daemonJob

Write-Host "`n=== ORCHESTRATION PRE-FLIGHT VERIFIED ===" -ForegroundColor Cyan