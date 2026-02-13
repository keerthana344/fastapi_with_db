$BackendDir = "C:\Users\student\Documents\fastapi_with_db"
Set-Location $BackendDir

# Start uvicorn in a new background process that is detached from the current shell
$processArgs = "-NoProfile -ExecutionPolicy Bypass -Command `".\env\Scripts\activate; uvicorn main:app --host 0.0.0.0 --port 8000`""
Start-Process powershell -ArgumentList $processArgs -WindowStyle Hidden

Write-Host "Backend starting in background on port 8000..."

