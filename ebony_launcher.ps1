# Purge any existing ghost processes
Get-Process | Where-Object {$_.Name -match "python"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Launch headless Python server (pythonw.exe leaves zero terminal footprint)
cd C:\HVF_Repos\hvf-media-matrix-private
Start-Process -FilePath "pythonw.exe" -ArgumentList "hvf_comm_server.py" -WindowStyle Hidden

# Launch the secure browser gate
Start-Process "http://127.0.0.1:8085"
