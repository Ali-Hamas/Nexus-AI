import asyncio
from app.services.mock_data import get_mock_snapshot, get_mock_diff
from app.services.replay import load_replay

def verify_mock_data():
    print("--- Verifying Mock Data Layer ---")
    snapshot = get_mock_snapshot("Notion", "pricing_change")
    assert snapshot["competitor_name"] == "Notion", "Competitor name mismatch"
    assert "pricing" in snapshot["scraped_data"], "Missing pricing data in mock"
    assert snapshot["raw_html_hash"] == "a1b2c3d4e5f6g7h8i9j0", "Hash mismatch"
    
    diff = get_mock_diff("tier_restructure")
    assert diff["confidence_score"] == 8.8, "Confidence score mismatch"
    assert "additions" in diff, "Missing additions in diff"
    print("Mock Data Layer: PASS")

def verify_replay_system():
    print("--- Verifying Replay System ---")
    data = load_replay("Slack", "feature_addition", "parsed_json")
    assert data != {}, "Failed to load replay data. Did the seed script run?"
    assert data["competitor_name"] == "Slack", "Replay data competitor name mismatch"
    print("Replay System: PASS")

if __name__ == "__main__":
    try:
        verify_mock_data()
        verify_replay_system()
        print("ALL PHASE 2 & 3 VERIFICATIONS PASSED.")
    except AssertionError as e:
        print(f"VERIFICATION FAILED: {e}")
