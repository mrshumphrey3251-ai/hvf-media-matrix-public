Write-Host "`n[ACTIVE AUDIO CAPTURE HARDWARE DETECTED]:" -ForegroundColor Cyan
Get-CimInstance Win32_SoundDevice | Select-Object Name, Status, DeviceID | Format-Table -AutoSize

# Open Windows Sound Settings directly to verify Default Input Device
Write-Host "[ACTION REQUIRED] Opening Windows Sound Control Panel..." -ForegroundColor Green
Write-Host "Ensure 'Headset (OpenRun by Shokz Hands-Free AG Audio)' is set as Default Input Device." -ForegroundColor Yellow
Start-Process "ms-settings:sound"
