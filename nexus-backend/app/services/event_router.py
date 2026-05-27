import hashlib
import json
from typing import Dict, Any

# Intelligent Cooldown Memory Store
_COOLDOWN_CACHE: Dict[str, str] = {}

class EventRouter:
    @staticmethod
    def is_in_cooldown(competitor: str, current_hash: str) -> bool:
        """
        Intelligent Cooldown Logic:
        If the exact same DOM structure was previously escalated, suppress continuous re-triggering.
        """
        last_escalated = _COOLDOWN_CACHE.get(competitor)
        if last_escalated == current_hash:
            return True
        return False

    @staticmethod
    def register_escalation(competitor: str, current_hash: str):
        _COOLDOWN_CACHE[competitor] = current_hash

    @staticmethod
    def evaluate_signal(scores: Dict[str, Any]) -> str:
        """
        Signal Severity Routing:
        Classifies the event severity based on impact and confidence scores.
        """
        impact = scores.get("impact_score", 0.0)
        confidence = scores.get("confidence_score", 0.0)
        
        if impact >= 8.5 and confidence >= 8.0:
            return "STRATEGIC EVENT"
        elif impact >= 6.0:
            return "MEDIUM SIGNAL"
        else:
            return "LOW SIGNAL"
            
    @staticmethod
    def should_escalate(scores: Dict[str, Any]) -> bool:
        """
        Signal Escalation Threshold: 75% (7.5 impact)
        """
        return scores.get("impact_score", 0.0) >= 7.5

event_router = EventRouter()
