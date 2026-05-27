import asyncio
from app.services.parser import compute_content_hash, process_guarded_inference

def verify_guarded_inference():
    print("--- Verifying Guarded Inference Layer ---")
    mock_content = "# Pricing\n\n$25/mo"
    mock_hash = compute_content_hash(mock_content)
    
    previous_snapshot = {
        "raw_html_hash": mock_hash
    }
    
    bypassed, current_hash, telemetry = process_guarded_inference(mock_content, previous_snapshot)
    
    assert bypassed == True, "Inference should have been bypassed"
    assert current_hash == mock_hash, "Hash mismatch"
    assert telemetry["inference_bypassed"] == True, "Telemetry mismatch"
    assert telemetry["tokens_saved"] > 0, "Token savings should be recorded"
    
    print(f"Bypass successful! Tokens saved: {telemetry['tokens_saved']}")
    print("Guarded Inference Layer: PASS")

if __name__ == "__main__":
    try:
        verify_guarded_inference()
        print("PHASE 5 VERIFICATION PASSED.")
    except AssertionError as e:
        print(f"VERIFICATION FAILED: {e}")
