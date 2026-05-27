from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright

from app.api.orchestrator import router as orchestrator_router
from app.api.events import router as events_router
from app.governance.review_queue import router as governance_router
from app.chaos.injector import router as chaos_router
from app.api.snapshots import router as snapshots_router
from app.api.simulation import router as simulation_router
from app.api.system import router as system_router
from app.services.watcher import watcher_service
from app.services.inference_router import inference_router
from app.db.models import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure SQLite tables exist
    print("Initializing SQLite schemas...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Stage 2: Proprietary Ingestion - Initialize persistent Playwright Chromium pool
    print("Initializing Proprietary Chromium Ingestion Pool...")
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    )
    # Anti-bot discipline: realistic viewport and user-agent
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        java_script_enabled=True,
        bypass_csp=True
    )
    
    # Expose to endpoints
    app.state.playwright = playwright
    app.state.browser = browser
    app.state.browser_context = context
    print("Ingestion Pool Ready.")
    
    # Stage 5: Cold Start Protection for Sovereign Inference
    await inference_router.warm_up()
    
    # Stage 4: Event-Driven Intelligence Activation
    print("Starting Continuous Intelligence Watcher...")
    watcher_service.start(app.state)
    print("Watcher Active.")
    
    yield
    
    # Graceful shutdown
    print("Shutting down Continuous Intelligence Watcher...")
    watcher_service.shutdown()
    print("Shutting down Ingestion Pool...")
    await context.close()
    await browser.close()
    await playwright.stop()

app = FastAPI(
    title="NEXUS Backend",
    description="Governed Event-Driven Intelligence Infrastructure",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Configuration for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orchestrator_router, prefix="/api/demo")
app.include_router(events_router, prefix="/api/demo")
app.include_router(governance_router, prefix="/api/governance")
app.include_router(chaos_router, prefix="/api/chaos")
app.include_router(snapshots_router, prefix="/api/system/snapshot")
app.include_router(system_router)
app.include_router(simulation_router)

@app.get("/health")
async def health_check():
    return {"status": "operational", "system": "NEXUS"}
