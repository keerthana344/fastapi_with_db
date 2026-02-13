Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File start_backend.ps1", 0
Set WshShell = Nothing
