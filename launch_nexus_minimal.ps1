# NEXUS: Demo-Day Minimal Boot Mode (Nuclear Survivability)
# This script launches the platform in a completely offline, deterministic mode.
# Use this if live ingestion or sovereign inference models fail during the presentation.
# It forces the system into Graceful Degradation using pre-seeded SQLite data.

echo "=== INITIATING NEXUS MINIMAL BOOT (DETERMINISTIC FAILOVER) ==="

# Force dead ports to trigger offline degradation automatically
$env:OLLAMA_HOST="http://localhost:9999"
$env:PLAYWRIGHT_OFFLINE="1"

# 1. Start Backend in background
echo "Booting Backend (Deterministic Mode)..."
cd nexus-backend
Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000"

# 2. Start Frontend
echo "Booting Frontend Dashboard..."
cd ..\nexus-frontend
npm run dev

echo "=== NEXUS MINIMAL BOOT ACTIVE ==="
