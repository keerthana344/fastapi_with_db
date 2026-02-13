$scriptsMatched = Get-WmiObject Win32_Process -Filter "Name LIKE '%python%' AND CommandLine LIKE '%uvicorn main:app%'"

if ($scriptsMatched) {
    foreach ($proc in $scriptsMatched) {
        Write-Host "Stopping process: $($proc.ProcessId)"
        Stop-Process -Id $proc.ProcessId -Force
    }
    Write-Host "Backend stopped successfully."
}
else {
    Write-Host "No running backend process found."
}
