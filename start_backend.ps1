$BackendDir = "C:\Users\student\Documents\fastapi_with_db"
cd $BackendDir

# Start uvicorn in a new background process (hidden window)
Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `".\env\Scripts\activate; uvicorn main:app --reload --host 0.0.0.0 --port 8000`"" -WindowStyle Hidden

Write-Host "Backend starting in background on port 8000..."
