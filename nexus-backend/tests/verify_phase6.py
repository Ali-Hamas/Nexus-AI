import asyncio
from app.services.engine import extract_semantic_intelligence, generate_semantic_diff, compute_dual_scores

async def verify_engine():
    print("--- Verifying Semantic Intelligence Engine ---")
    
    # 1. Test Mock Extraction (No Key Fallback)
    mock_md = "# Pricing\n\nPro: $20/mo\nEnterprise: Contact Us"
    extracted = await extract_semantic_intelligence(mock_md)
    assert "pricing" in extracted, "Failed to extract structured pricing"
    
    # 2. Test Semantic Diff
    hist = {
        "pricing": [{"tier_name": "Pro", "price": "$20/mo"}],
        "features": ["SSO"]
    }
    curr = {
        "pricing": [{"tier_name": "Pro", "price": "$25/mo"}],
        "features": ["SSO", "Analytics"]
    }
    
    diff = generate_semantic_diff(curr, hist)
    assert "pricing" in diff["additions"] and "Pro" in diff["additions"]["pricing"], "Failed to detect price increase"
    assert "Analytics" in diff["additions"]["features"], "Failed to detect new feature"
    
    # 3. Test Dual Scoring
    scores = compute_dual_scores(diff)
    assert scores["impact_score"] >= 8.0, "Pricing change should be high impact"
    assert "confidence_reason" in scores, "Explainability metadata missing"
    
    print("Semantic Extraction: PASS")
    print("Semantic Diff Engine: PASS")
    print("Dual Scoring Engine: PASS")

if __name__ == "__main__":
    try:
        asyncio.run(verify_engine())
        print("PHASE 6 VERIFICATION PASSED.")
    except AssertionError as e:
        print(f"VERIFICATION FAILED: {e}")
