import hashlib
from typing import List, Dict, Any, Tuple

class TrajectoryType:
    REINFORCEMENT = "REINFORCEMENT" # existing trend intensifies
    DIVERGENCE = "DIVERGENCE" # sector fragmentation
    COMPRESSION = "COMPRESSION" # feature parity collapse
    ESCALATION = "ESCALATION" # volatility amplification
    STABILIZATION = "STABILIZATION" # convergence decay

class TrajectoryCollisionDetector:
    """Future-state arbitration. Detects incompatible futures."""
    
    @staticmethod
    def evaluate_trajectories(trajectories: List[str]) -> Tuple[bool, float]:
        """
        Returns (is_stable, contradiction_penalty).
        """
        contradiction_penalty = 0.0
        
        # Example constraints: You can't have both Stabilization and Escalation
        if TrajectoryType.STABILIZATION in trajectories and TrajectoryType.ESCALATION in trajectories:
            contradiction_penalty += 45.0
            
        # You can't have Divergence and Compression simultaneously
        if TrajectoryType.DIVERGENCE in trajectories and TrajectoryType.COMPRESSION in trajectories:
            contradiction_penalty += 30.0
            
        is_stable = contradiction_penalty < 20.0
        return is_stable, contradiction_penalty

def generate_trajectory_hash(trajectories: List[str]) -> str:
    """Generates a replayable fingerprint for the selected trajectories."""
    payload = ",".join(sorted(trajectories))
    return hashlib.sha256(payload.encode()).hexdigest()
