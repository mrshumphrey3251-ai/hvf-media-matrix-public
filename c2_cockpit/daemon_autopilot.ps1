# E.B.O.N.Y. Autonomous Travel Autopilot Loop Daemon (Headless Logger)
# Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5
$pythonExe = "C:\Users\mrshu\AppData\Local\Programs\Python\Python311\python.exe"
$scriptPath = "C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_travel_autopilot.py"
$logPath = "C:\hvf_c2\hvf-media-matrix-private\autopilot_daemon.log"
$env:PYTHONIOENCODING = "utf-8"

$header = "[$( (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss UTC') )] [DAEMON_BOOT] E.B.O.N.Y. Travel Autopilot Service Initialized. 300s Cadence."
Add-Content -Path $logPath -Value $header

while ($true) {
    $now = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd HH:mm:ss UTC")
    Add-Content -Path $logPath -Value "`n[$now] Executing autonomous travel sweep..."
    try {
        & $pythonExe $scriptPath --send 2>&1 | Out-File -FilePath $logPath -Append -Encoding utf8
    } catch {
        Add-Content -Path $logPath -Value "[$now] [ERROR] Sweep failed: $_"
    }
    Start-Sleep -Seconds 300
}