Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""[REDACTED-PRIVATE-ROOT]\ebony_launcher.ps1""", 0, False
