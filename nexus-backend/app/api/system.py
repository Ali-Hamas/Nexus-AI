from fastapi import APIRouter, Depends
from app.auth.roles import require_role, Role
from app.config.settings import settings
import app.api.simulation as simulation_api

router = APIRouter(prefix="/api/system", tags=["System"])

@router.get("/state")
async def get_system_state(role: Role = Depends(require_role(Role.SYSTEM_ADMIN))):
    """
    Exposes infrastructure observability and resource budgets.
    Requires SYSTEM_ADMIN role.
    """
    return {
        "status": "success",
        "system_state": settings.SYSTEM_STATE,
        "resource_budgets": {
            "max_parallel_sandboxes": settings.MAX_PARALLEL_SANDBOXES,
            "max_pending_simulations": settings.MAX_PENDING_SIMULATIONS,
            "max_graph_mutations": settings.MAX_GRAPH_MUTATIONS,
            "max_concurrent_inference": settings.MAX_CONCURRENT_INFERENCE
        },
        "current_usage": {
            "active_sandboxes": simulation_api.active_sandboxes,
            "queued_sandboxes": simulation_api.queued_sandboxes,
            "active_inference_slots": 0 # Mock for now
        },
        "epochs": {
            "constitution": settings.CONSTITUTION_VERSION,
            "schema": settings.SCHEMA_EPOCH,
            "governance": settings.GOVERNANCE_EPOCH
        }
    }
