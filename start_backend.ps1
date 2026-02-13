$BackendDir = "C:\Users\student\Documents\fastapi_with_db"
Set-Location $BackendDir

# Start uvicorn using the absolute path to the virtual environment's python and redirect output to a log file
$uvicornPath = ".\env\Scripts\uvicorn.exe"
$logFile = "backend.log"
$processArgs = "-NoProfile -ExecutionPolicy Bypass -Command `"$uvicornPath main:app --host 0.0.0.0 --port 8000 > $logFile 2>&1`""
Start-Process powershell -ArgumentList $processArgs -WindowStyle Hidden

Write-Host "Backend starting in background on port 8000. Logs at $logFile"


