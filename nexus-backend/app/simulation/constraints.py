import hashlib
import json
from typing import Dict, Any, Tuple

class SimulationDecayCurve:
    """Mathematically degrades max confidence based on Horizon."""
    @staticmethod
    def get_max_confidence(horizon: str) -> float:
        if horizon == "SHORT":
            return 95.0
        elif horizon == "MEDIUM":
            return 75.0
        elif horizon == "LONG":
            return 45.0
        return 0.0 # Invalid horizon

class ConstitutionalValidator:
    """Pre-Simulation Constitutional Validation."""
    @staticmethod
    def validate(mutation_type: str, horizon: str) -> Tuple[bool, str]:
        if not mutation_type:
            return False, "Mutation type cannot be empty (Open-ended prompts forbidden by Constitution)."
        if horizon not in ["SHORT", "MEDIUM", "LONG"]:
            return False, f"Horizon {horizon} is outside institutional bounds."
        return True, "Constitutional bounds validated."

class ConstraintEngine:
    """Enforces minimum integrity and evidence density for simulations."""
    def __init__(self, min_integrity: float = 80.0, min_evidence_density: float = 3.0, max_contradiction_pressure: float = 2.0):
        self.min_integrity = min_integrity
        self.min_evidence_density = min_evidence_density
        self.max_contradiction_pressure = max_contradiction_pressure

    def evaluate_sandbox_state(self, graph_metrics: Dict[str, Any]) -> Tuple[bool, str]:
        if graph_metrics.get("integrity_score", 0) < self.min_integrity:
            return False, f"Graph integrity {graph_metrics.get('integrity_score')} below minimum {self.min_integrity}."
        
        if graph_metrics.get("evidence_density", 0) < self.min_evidence_density:
            return False, f"Evidence density {graph_metrics.get('evidence_density')} below minimum {self.min_evidence_density}."
            
        if graph_metrics.get("contradiction_pressure", 0) > self.max_contradiction_pressure:
            return False, f"Contradiction pressure {graph_metrics.get('contradiction_pressure')} exceeds maximum {self.max_contradiction_pressure}."
            
        return True, "Constraint engine passed."

def generate_constraint_hash(params: Dict[str, Any]) -> str:
    """Generates a replayable fingerprint of the constraint set."""
    payload = json.dumps(params, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()
