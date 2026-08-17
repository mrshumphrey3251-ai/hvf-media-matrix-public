$host.UI.RawUI.WindowTitle = 'Ebony Live Production Server'
Write-Host "[*] Initiating Sovereign Ignition Sequence..." -ForegroundColor Cyan

# Purge any ghost processes
Get-Process | Where-Object {$_.Name -match "python"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Launch the browser
Start-Process "http://127.0.0.1:8085"

# Boot the server
cd C:\HVF_Repos\hvf-media-matrix-private
python hvf_comm_server.py
