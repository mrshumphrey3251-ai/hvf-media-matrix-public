Set WshShell = CreateObject("WScript.Shell")
' The 0 completely disables console allocation. False means don't wait for it to finish.
WshShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\HVF_Repos\hvf-media-matrix-private\ebony_launcher.ps1""", 0, False
