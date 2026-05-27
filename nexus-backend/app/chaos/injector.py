import logging
from fastapi import APIRouter, Depends
from app.events.bus import distributed_bus
from app.schemas.intelligence import CanonicalIntelligenceEvent, EventMode, LifecycleState
from app.auth.roles import require_role, Role, MIN_ROLE_FOR_CHAOS_EXECUTION

logger = logging.getLogger(__name__)
router = APIRouter()

class ChaosInjector:
    """
    Distributed Cognition Failure Simulation.
    Simulates graph contradictions, governance deadlocks, event duplication,
    scheduler starvation, and priority inversions.
    """
    
    async def inject_graph_contradiction(self):
        """Simulates mutually exclusive graph edges being introduced simultaneously."""
        logger.warning("[CHAOS] Injecting Graph Contradiction")
        event = CanonicalIntelligenceEvent(
            sector="Productivity SaaS",
            target="Notion",
            action="GRAPHED",
            message="[CHAOS] Simulated contradiction: Notion dropping AI features while launching AI suite.",
            priority_score=95.0,
            event_mode=EventMode.CHAOS.value,
            event_lifecycle_state=LifecycleState.GRAPHED.value,
            payload={"contradiction": "mutually_exclusive_pricing_tier"}
        )
        await distributed_bus.publish("watcher_feed", event.dict())
        return {"status": "injected", "type": "graph_contradiction"}

    async def inject_governance_deadlock(self):
        """Simulates an escalated review item that receives conflicting verification inputs."""
        logger.warning("[CHAOS] Injecting Governance Deadlock")
        event = CanonicalIntelligenceEvent(
            sector="Productivity SaaS",
            target="Notion",
            action="ESCALATED",
            message="[CHAOS] Simulated governance deadlock in adjudication queue.",
            priority_score=80.0,
            event_mode=EventMode.CHAOS.value,
            event_lifecycle_state=LifecycleState.REVIEW_REQUIRED.value
        )
        await distributed_bus.publish("events.governance", event.dict())
        return {"status": "injected", "type": "governance_deadlock"}
        
    async def inject_inference_timeout(self):
        """Simulates a sovereign LLaMA-3 inference failure, forcing Deterministic Recovery."""
        logger.warning("[CHAOS] Injecting Inference Timeout")
        event = CanonicalIntelligenceEvent(
            sector="Dev Tools",
            target="GitHub",
            action="SYNTHESIS_TIMEOUT",
            message="[CHAOS] Forced sovereign model timeout. Forcing Graceful Degradation.",
            priority_score=90.0,
            event_mode=EventMode.CHAOS.value,
            event_lifecycle_state=LifecycleState.SYNTHESIZED.value
        )
        await distributed_bus.publish("watcher_feed", event.dict())
        return {"status": "injected", "type": "inference_timeout"}

    async def inject_multi_brief_conflict(self):
        """Simulates Institutional Contradiction Arbitration (Multi-Brief Conflict)."""
        logger.warning("[CHAOS] Injecting Multi-Brief Governance Conflict")
        
        # Brief A: AI Acceleration
        brief_a = CanonicalIntelligenceEvent(
            sector="Productivity SaaS",
            target="Notion",
            action="ESCALATED",
            message="[CHAOS] Brief A: AI Acceleration detected.",
            priority_score=90.0,
            event_mode=EventMode.CHAOS.value,
            event_lifecycle_state=LifecycleState.REVIEW_REQUIRED.value
        )
        
        # Brief B: Market Deceleration (Contradiction)
        brief_b = CanonicalIntelligenceEvent(
            sector="Productivity SaaS",
            target="Notion",
            action="ESCALATED",
            message="[CHAOS] Brief B: Market Deceleration detected. (Contradicts Brief A)",
            priority_score=95.0, # Higher priority contradiction
            event_mode=EventMode.CHAOS.value,
            event_lifecycle_state=LifecycleState.REVIEW_REQUIRED.value
        )
        
        await distributed_bus.publish("events.governance", brief_a.dict())
        await distributed_bus.publish("events.governance", brief_b.dict())
        return {"status": "injected", "type": "multi_brief_conflict"}

    async def inject_queue_saturation(self):
        """Simulates Governance Queue Saturation."""
        logger.warning("[CHAOS] Injecting Queue Saturation")
        from app.config.settings import settings
        settings.SYSTEM_STATE = settings.STATE_GOVERNANCE_FROZEN
        for i in range(50):
            event = CanonicalIntelligenceEvent(
                sector="Simulated",
                target=f"Target-{i}",
                action="SYNTHESIZED",
                message=f"[CHAOS] Saturation Event {i}",
                event_mode=EventMode.CHAOS.value,
                event_lifecycle_state=LifecycleState.REVIEW_REQUIRED.value
            )
            await distributed_bus.publish("events.governance", event.dict())
        return {"status": "injected", "type": "queue_saturation"}

chaos_engine = ChaosInjector()

@router.post("/inject/contradiction")
async def api_inject_contradiction(role: Role = Depends(require_role(MIN_ROLE_FOR_CHAOS_EXECUTION))):
    return await chaos_engine.inject_graph_contradiction()

@router.post("/inject/deadlock")
async def api_inject_deadlock(role: Role = Depends(require_role(MIN_ROLE_FOR_CHAOS_EXECUTION))):
    return await chaos_engine.inject_governance_deadlock()

@router.post("/inject/timeout")
async def api_inject_timeout(role: Role = Depends(require_role(MIN_ROLE_FOR_CHAOS_EXECUTION))):
    return await chaos_engine.inject_inference_timeout()

@router.post("/inject/conflict")
async def api_inject_conflict(role: Role = Depends(require_role(MIN_ROLE_FOR_CHAOS_EXECUTION))):
    return await chaos_engine.inject_multi_brief_conflict()

@router.post("/inject/saturation")
async def api_inject_saturation(role: Role = Depends(require_role(MIN_ROLE_FOR_CHAOS_EXECUTION))):
    return await chaos_engine.inject_queue_saturation()
