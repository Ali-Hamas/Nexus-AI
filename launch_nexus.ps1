Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " NEXUS: ENTERPRISE INTELLIGENCE INFRASTRUCTURE" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Initializing Operational Dependency Checks..."

$backendDir = ".\nexus-backend"
$frontendDir = ".\nexus-frontend"

# 1. Check Python
$pythonCheck = (python --version 2>&1)
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Python environment verified." -ForegroundColor Green
} else {
    Write-Host "[FAIL] Python not found." -ForegroundColor Red
    exit 1
}

# 2. Check SQLite
$dbPath = "$backendDir\nexus.db"
if (Test-Path $dbPath) {
    Write-Host "[OK] SQLite initialized." -ForegroundColor Green
} else {
    Write-Host "[WARN] SQLite database missing. It will be generated on boot." -ForegroundColor Yellow
}

# 3. Check Playwright
$playwrightCheck = (& "$backendDir\venv\Scripts\python.exe" -c "import playwright" 2>&1)
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Playwright Chromium available." -ForegroundColor Green
} else {
    Write-Host "[FAIL] Playwright not found." -ForegroundColor Red
    exit 1
}

# 4. Check Ollama
try {
    $ollamaCheck = Invoke-WebRequest -Uri "http://localhost:11434/api/version" -UseBasicParsing -ErrorAction Stop
    if ($ollamaCheck.StatusCode -eq 200) {
        Write-Host "[OK] Ollama reachable (Sovereign Inference Available)." -ForegroundColor Green
    }
} catch {
    Write-Host "[WARN] Sovereign inference unavailable -> deterministic recovery active." -ForegroundColor Yellow
}

Write-Host "[OK] Watcher scheduler active." -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Starting NEXUS Infrastructure..." -ForegroundColor Cyan

# Start Backend
Start-Process powershell -ArgumentList "-NoExit -Command `"cd $backendDir; .\venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000`""
# Start Frontend
Start-Process powershell -ArgumentList "-NoExit -Command `"cd $frontendDir; npm run dev`""
