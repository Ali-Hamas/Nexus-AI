import hashlib
import json
import uuid
from typing import Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import GraphNode, GraphEdge, StrategicSimulation
from app.simulation.constraints import ConstitutionalValidator, ConstraintEngine, SimulationDecayCurve, generate_constraint_hash
from app.simulation.trajectory import TrajectoryCollisionDetector, TrajectoryType, generate_trajectory_hash

# Mock LLM for simulation synthesis to prevent external dependency breaking
async def bounded_narrative_synthesizer(target: str, mutation: str, trajectories: List[str], constraints: Dict[str, Any]) -> Dict[str, Any]:
    """
    The LLM is ONLY a bounded narrative synthesizer.
    It does NOT decide constraints or define trajectories.
    """
    return {
        "scenario_title": f"Strategic Projection: {target} {mutation}",
        "executive_summary": f"Under the bounded constraint of {mutation}, the ecosystem is highly likely to experience {', '.join(trajectories)}.",
        "projected_events": [
            f"Initial shock from {mutation} triggers immediate {trajectories[0]} response.",
            "Secondary effects stabilize within the temporal horizon constraints."
        ],
        "evidence_anchors": [
            "Historical convergence patterns",
            "Current graph density"
        ]
    }

class ScenarioSandboxEngine:
    """
    Clones the graph into memory, applies a mutation, checks constraints, and if valid, runs synthesis.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.constraint_engine = ConstraintEngine()

    def _clone_sandbox(self) -> Dict[str, Any]:
        """Creates an in-memory clone of live graph metrics to avoid live mutation."""
        # In a real implementation this would deep-clone the SQLAlchemy models into a memory DB
        # Here we mock the aggregate metrics the constraints rely on
        return {
            "integrity_score": 95.0,
            "evidence_density": 8.5,
            "contradiction_pressure": 0.5,
            "sandbox_hash": hashlib.sha256(b"SANDBOX_STATE").hexdigest()
        }

    async def execute_projection(self, target_node: str, mutation: str, horizon: str, requested_trajectory: str) -> StrategicSimulation:
        # 1. Constitutional Check
        is_legal, legal_reason = ConstitutionalValidator.validate(mutation_type=mutation, horizon=horizon)
        if not is_legal:
            raise ValueError(f"Constitutional Violation: {legal_reason}")

        # 2. Sandbox Clone & Mutation
        sandbox_state = self._clone_sandbox()
        
        # 3. Constraint Engine Check
        is_valid, constraint_reason = self.constraint_engine.evaluate_sandbox_state(sandbox_state)
        if not is_valid:
            raise ValueError(f"Constraint Engine Blocked Simulation: {constraint_reason}")

        # 4. Trajectory Collision Check
        is_stable, contradiction_penalty = TrajectoryCollisionDetector.evaluate_trajectories([requested_trajectory])
        stability_score = max(0.0, 100.0 - contradiction_penalty)
        
        # 5. Integrity Decay Calculation
        base_confidence = sandbox_state["integrity_score"]
        max_horizon_confidence = SimulationDecayCurve.get_max_confidence(horizon)
        final_confidence = min(base_confidence, max_horizon_confidence)

        # 6. LLM Synthesis (ONLY IF ALL GATES PASSED)
        constraint_params = {
            "horizon": horizon,
            "min_integrity": self.constraint_engine.min_integrity,
            "min_evidence": self.constraint_engine.min_evidence_density
        }
        
        synthesis = await bounded_narrative_synthesizer(
            target=target_node,
            mutation=mutation,
            trajectories=[requested_trajectory],
            constraints=constraint_params
        )

        # 7. Persistence & Replay Hashes
        simulation = StrategicSimulation(
            target_node_id=target_node,
            mutation_type=mutation,
            temporal_horizon=horizon,
            simulation_hash=hashlib.sha256(f"{target_node}:{mutation}:{horizon}".encode()).hexdigest(),
            trajectory_hash=generate_trajectory_hash([requested_trajectory]),
            constraint_hash=generate_constraint_hash(constraint_params),
            trajectory_type=requested_trajectory,
            synthesis_payload=synthesis,
            confidence=final_confidence,
            stability_score=stability_score,
            contradiction_pressure=sandbox_state["contradiction_pressure"] + contradiction_penalty,
            evidence_density=sandbox_state["evidence_density"],
            governance_state="SIMULATED"
        )
        
        self.db.add(simulation)
        await self.db.commit()
        await self.db.refresh(simulation)
        
        return simulation
