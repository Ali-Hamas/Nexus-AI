import hashlib
import json
import time
from typing import Dict, Any, Tuple

# =========================================================================
# NEXUS - GUARDED INFERENCE LAYER
# =========================================================================

def compute_content_hash(content: str) -> str:
    """Generates a SHA-256 hash of the raw markdown content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def should_bypass_inference(current_hash: str, previous_snapshot: Dict[str, Any]) -> bool:
    """
    Compares the current hash against the historical snapshot.
    Returns True if the content is completely unchanged, saving tokens and latency.
    """
    if not previous_snapshot:
        return False
        
    previous_hash = previous_snapshot.get("raw_html_hash")
    return current_hash == previous_hash

def process_guarded_inference(content: str, previous_snapshot: Dict[str, Any] = None) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Executes the guarded inference pipeline.
    Returns: (inference_bypassed: bool, current_hash: str, telemetry: dict)
    """
    start_time = time.time()
    
    current_hash = compute_content_hash(content)
    
    # Check if we can bypass expensive GPT processing
    inference_bypassed = should_bypass_inference(current_hash, previous_snapshot)
    
    latency_ms = int((time.time() - start_time) * 1000)
    
    # Telemetry metrics to pass to the UI
    telemetry = {
        "hash_computation_latency_ms": latency_ms,
        "inference_bypassed": inference_bypassed,
        # Rough token estimation (1 token ~= 4 chars)
        "tokens_saved": len(content) // 4 if inference_bypassed else 0
    }
    
    return inference_bypassed, current_hash, telemetry
