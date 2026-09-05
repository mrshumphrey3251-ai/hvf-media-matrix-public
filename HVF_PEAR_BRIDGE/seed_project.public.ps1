<#
.SYNOPSIS
    Project Ebony: Sovereign Pear Native Seeder (Public Blueprint)
    Executes directly in authenticated shell environment.
    Author: Jeffery Humphrey, CEO & Apex Architect
#>

$ErrorActionPreference = "Stop"
$PEAR_LINK = "pear://<PROJECT_LINK_REDACTED>"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " PROJECT EBONY: NATIVE PEAR DHT SEED CONTROLLER (PUBLIC)" -ForegroundColor Cyan
Write-Host " Status: Iron Dome Compliant" -ForegroundColor Green
Write-Host " Link: $PEAR_LINK" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan

pear seed --no-tty $PEAR_LINK
