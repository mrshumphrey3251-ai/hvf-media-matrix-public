Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\HVF_Repos\hvf-media-matrix-private\ebony_launcher.ps1""", 0, False
