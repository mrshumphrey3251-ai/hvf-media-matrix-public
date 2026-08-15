$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\HVF_Repos\hvf-media-matrix-private\generate_batch_dispatches.py" -WorkingDirectory "C:\HVF_Repos\hvf-media-matrix-private"
$trigger = New-ScheduledTaskTrigger -Daily -At "06:00AM"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "HVF_Matrix_Daily_Dispatch_Refresh" -Action $action -Trigger $trigger -Settings $settings -Description "Daily refresh of HVF Media Matrix Scheduled Dispatch Queue" -Force -ErrorAction SilentlyContinue
Write-Host "[*] Automated Task Scheduled: HVF_Matrix_Daily_Dispatch_Refresh registered for 06:00 AM daily."
