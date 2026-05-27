import asyncio
from httpx import AsyncClient
from app.main import app

async def verify_orchestrator():
    print("--- Verifying Orchestrator Layer ---")
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/demo/run", json={
            "competitor": "Notion",
            "url": "https://notion.so/pricing",
            "force_fallback": True, # Ensure it uses our seeded replay data
            "scenario": "tier_restructure"
        })
        
    assert response.status_code == 200, f"Request failed: {response.status_code}"
    data = response.json()
    
    assert data["status"] == "success", "Response status is not success"
    assert data["mode"] == "FALLBACK", "Did not enter fallback mode"
    assert "additions" in data["diff"], "Diff data is missing"
    assert "impact_score" in data["scores"], "Scores are missing"
    assert data["pdf_url"] is not None, "PDF generation failed in orchestration"
    
    print("Orchestrator integration successfully executed the fallback pipeline.")
    print("Orchestrator Layer: PASS")

if __name__ == "__main__":
    try:
        asyncio.run(verify_orchestrator())
        print("PHASE 8 VERIFICATION PASSED.")
    except AssertionError as e:
        print(f"VERIFICATION FAILED: {e}")
