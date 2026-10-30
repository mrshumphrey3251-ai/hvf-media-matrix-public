# -*- coding: utf-8 -*-
# HUMPHREY VIRTUAL FARMS LLC // ONE-CLICK DESKTOP SOVEREIGN AUTO-PUBLISHER CONSOLE
# Entity: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
# Active Docket: 10-26-4046 (04:24 Master Video SHA-256: c597865785eae6fdad6fdf6803a2710aaa0fb5c2fa28fe512b6ed76ef8b7a7fd)

$Host.UI.RawUI.WindowTitle = "HVF SOVEREIGN C2 // DUAL-GITHUB AUTO-PUBLISHER (DOCKET 10-26-4046)"
Set-Location "C:\hvf_c2\hvf-media-matrix-private"

Write-Host "==========================================================================================" -ForegroundColor Cyan
Write-Host "  HUMPHREY VIRTUAL FARMS LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)" -ForegroundColor Green
Write-Host "  ONE-CLICK SOVEREIGN DUAL-GITHUB AUTO-PUBLISHER & 85/85 TEST VERIFIER" -ForegroundColor Green
Write-Host "  Active TSM Docket: 10-26-4046 | Master Video: 04:24 (264.23s)" -ForegroundColor Yellow
Write-Host "==========================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "SELECT EXECUTION MODE:" -ForegroundColor White
Write-Host "  [1] Instant Dual-Repo Sync, Schema Heal & 85/85 Test Verification (Press ENTER or 1)" -ForegroundColor Green
Write-Host "  [2] Auto-Publish a New Proposal / Memo Text to Private & Redacted Public GitHub" -ForegroundColor Cyan
Write-Host "  [3] Auto-Publish an Existing File (.md / .txt) to Private & Redacted Public GitHub" -ForegroundColor Cyan
Write-Host "  [4] Update Active Docket ID Globally Across Both Repositories" -ForegroundColor Yellow
Write-Host ""

$Choice = Read-Host "Enter choice (Default = 1)"
if ([string]::IsNullOrWhiteSpace($Choice)) { $Choice = "1" }

if ($Choice -eq "1") {
    Write-Host "`nRunning Full Sovereign Sync, Schema Heal, 85/85 Tests & Dual GitHub Push..." -ForegroundColor Green
    .\Publish-HVF.ps1
}
elseif ($Choice -eq "2") {
    $Title = Read-Host "`nEnter Proposal or Record Title"
    $Body  = Read-Host "Paste or Type Body Text"
    if ($Title -and $Body) {
        Write-Host "`nPublishing to Private (Unredacted) & Public (Auto-Redacted) GitHub Repositories..." -ForegroundColor Green
        .\Publish-HVF.ps1 -Title $Title -Body $Body
    } else {
        Write-Host "Aborted: Both Title and Body Text are required for Mode 2." -ForegroundColor Red
    }
}
elseif ($Choice -eq "3") {
    $Title    = Read-Host "`nEnter Proposal or Record Title"
    $FilePath = Read-Host "Enter Full Path to File (.md or .txt)"
    $FilePath = $FilePath.Trim('"')
    if ($Title -and (Test-Path $FilePath)) {
        Write-Host "`nIngesting file and publishing to Private & Public GitHub Repositories..." -ForegroundColor Green
        .\Publish-HVF.ps1 -Title $Title -BodyFile $FilePath
    } else {
        Write-Host "Aborted: Valid Title and existing File Path are required for Mode 3." -ForegroundColor Red
    }
}
elseif ($Choice -eq "4") {
    $NewDocket = Read-Host "`nEnter New Active Docket ID (e.g., 10-26-XXXX)"
    if ($NewDocket) {
        Write-Host "`nSynchronizing all files and filenames to Docket $NewDocket..." -ForegroundColor Green
        .\Publish-HVF.ps1 -Docket $NewDocket
    }
}

Write-Host ""
Write-Host "==========================================================================================" -ForegroundColor Cyan
Read-Host "EXECUTION COMPLETE. Press ENTER to close this Command Console"
