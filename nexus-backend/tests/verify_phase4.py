import asyncio
from app.services.fetcher import safe_fetch_pipeline

async def verify_fetcher():
    print("--- Verifying Bright Data Fetcher Layer ---")
    # This should fail instantly and return FALLBACK because credentials are the default placeholders
    result = await safe_fetch_pipeline("Notion", "https://notion.so/pricing", None)
    
    assert result["mode"] == "FALLBACK", f"Expected FALLBACK mode, got {result['mode']}"
    assert result["error"] is not None, "Expected an error message"
    print(f"Fallback caught correctly with error: {result['error']}")
    print("Fetcher Layer: PASS")

if __name__ == "__main__":
    try:
        asyncio.run(verify_fetcher())
        print("PHASE 4 VERIFICATION PASSED.")
    except AssertionError as e:
        print(f"VERIFICATION FAILED: {e}")
