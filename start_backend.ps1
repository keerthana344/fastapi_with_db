$BackendDir = "C:\Users\student\Documents\fastapi_with_db"
Set-Location $BackendDir

# Start uvicorn using the absolute path to the virtual environment's python to avoid environment mismatches
$uvicornPath = ".\env\Scripts\uvicorn.exe"
$processArgs = "-NoProfile -ExecutionPolicy Bypass -Command `"$uvicornPath main:app --host 0.0.0.0 --port 8000`""
Start-Process powershell -ArgumentList $processArgs -WindowStyle Hidden

Write-Host "Backend starting in background on port 8000 using local environment..."

