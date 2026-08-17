$Host.UI.RawUI.WindowTitle = 'HVF Ebony Sovereign Server Core'
Clear-Host
Write-Host "========================================================" -ForegroundColor DarkGray
Write-Host " HVF EBONY ENGINE DIAGNOSTIC CONSOLE" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor DarkGray

# Check if Python is accessible
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) {
    Write-Host "[!] CRITICAL: Python executable not found in system PATH." -ForegroundColor Red
    Read-Host -Prompt "Press Enter to exit"
    Exit
}

Write-Host "[+] Python engine located: $pythonPath" -ForegroundColor Green
Write-Host "[*] Launching Flask Server Application..." -ForegroundColor Cyan

# Navigate to repository and run Python, keeping the window alive to print errors
cd "C:\HVF_Repos\hvf-media-matrix-private"
python app.py

Write-Host "
[!] CRITICAL: Python application crashed or exited unexpectedly." -ForegroundColor Red
Read-Host -Prompt "Press Enter to close window"
