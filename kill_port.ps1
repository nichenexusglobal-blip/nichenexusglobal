$pids = @(Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess)
if ($pids.Count -gt 0) {
    foreach ($p in $pids) {
        try {
            Stop-Process -Id $p -Force -ErrorAction Stop
            Write-Output "Killed PID $p on port 3000"
        } catch {
            Write-Output "Failed to kill PID $p: $_"
        }
    }
} else {
    Write-Output "No process found on port 3000"
}
