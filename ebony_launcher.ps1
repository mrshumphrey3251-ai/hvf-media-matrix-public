# 1. Neutralize background ghost engines
Get-Process | Where-Object {$_.Name -match "python"} | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Launch the monolithic server directly in the background (Invisible)
Start-Process python -ArgumentList "app.py" -WorkingDirectory "C:\HVF_Repos\hvf-media-matrix-private" -WindowStyle Hidden

# 3. Wait 2 seconds for engine ignition
Start-Sleep -Seconds 2

# 4. Generate random cryptographic override to shatter browser cache
$CacheBuster = Get-Random

# 5. Open the web browser securely forcing a live fetch
Start-Process "http://127.0.0.1:5000/?override=$CacheBuster"
