# 1. Neutralize background ghost engines
Get-Process | Where-Object {$_.Name -match "python"} | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Launch the monolithic server directly in the background (Invisible)
Start-Process python -ArgumentList "app.py" -WorkingDirectory "C:\HVF_Repos\hvf-media-matrix-private" -WindowStyle Hidden

# 3. Wait 2 seconds for engine ignition
Start-Sleep -Seconds 2

# 4. Open the web browser securely to the local dashboard
Start-Process "http://127.0.0.1:5000"
