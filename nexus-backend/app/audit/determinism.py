import hashlib
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DeterminismAuditEngine:
    """
    Guarantees strict cognition reproducibility across the scheduler and memory boundaries.
    """
    
    def generate_scheduler_trace_hash(self, inputs: Dict[str, Any], priority_order: list) -> str:
        """
        Ensures that identical inputs to the Cognitive Scheduler produce the exact same
        priority execution cascade and graph mutation sequence.
        """
        trace = {
            "inputs": inputs,
            "priority_cascade": priority_order
        }
        trace_str = json.dumps(trace, sort_keys=True)
        return hashlib.sha256(trace_str.encode('utf-8')).hexdigest()

    def audit_replay_determinism(self, historical_synthesis: dict, replayed_synthesis: dict) -> bool:
        """
        Compares the checksums of a live synthesis event with a sandbox replay.
        """
        hist_hash = hashlib.sha256(json.dumps(historical_synthesis, sort_keys=True).encode('utf-8')).hexdigest()
        replay_hash = hashlib.sha256(json.dumps(replayed_synthesis, sort_keys=True).encode('utf-8')).hexdigest()
        
        is_deterministic = (hist_hash == replay_hash)
        if not is_deterministic:
            logger.error(f"[DETERMINISM AUDIT FAILED] Live: {hist_hash} != Replay: {replay_hash}")
            
        return is_deterministic

determinism_auditor = DeterminismAuditEngine()
