import logging
import json
from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from app.db.models import AsyncSessionLocal, PlatformSnapshot, GraphNode, GraphEdge, GovernanceReview, WebSnapshot
from app.config.settings import settings
from app.auth.roles import require_role, Role

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/export")
async def export_snapshot(
    description: str = "Manual Platform Snapshot",
    role: Role = Depends(require_role(Role.SYSTEM_ADMIN))
):
    """
    Creates a full institutional state snapshot (SQLite primary storage).
    Serializes the entire memory graph and governance queue.
    """
    async with AsyncSessionLocal() as db:
        # 1. Serialize Graph Nodes
        nodes_result = await db.execute(select(GraphNode))
        nodes = [{"id": n.id, "node_type": n.node_type, "name": n.name, "sector": n.sector, "attributes": n.attributes} for n in nodes_result.scalars().all()]
        
        # 2. Serialize Graph Edges
        edges_result = await db.execute(select(GraphEdge))
        edges = [{"id": e.id, "source_id": e.source_id, "target_id": e.target_id, "relationship_type": e.relationship_type, "strength": e.strength, "confidence": e.confidence, "evidence_density": e.evidence_density} for e in edges_result.scalars().all()]
        
        # 3. Serialize Governance Reviews
        gov_result = await db.execute(select(GovernanceReview))
        governance = [{"id": g.id, "status": g.status, "brief_data": g.brief_data, "priority_score": g.priority_score, "integrity_score": g.integrity_score} for g in gov_result.scalars().all()]
        
        state_payload = {
            "graph_nodes": nodes,
            "graph_edges": edges,
            "governance_queue": governance
        }
        
        snapshot = PlatformSnapshot(
            snapshot_type="FULL_STATE",
            description=description,
            state_payload=state_payload,
            constitution_version=settings.CONSTITUTION_VERSION,
            schema_epoch=settings.SCHEMA_EPOCH,
            governance_epoch=settings.GOVERNANCE_EPOCH
        )
        
        db.add(snapshot)
        await db.commit()
        await db.refresh(snapshot)
        
        logger.info(f"Platform Snapshot {snapshot.id} created successfully.")
        return {"status": "success", "snapshot_id": snapshot.id, "epoch": settings.SCHEMA_EPOCH}

@router.get("/export/{snapshot_id}/json")
async def export_snapshot_json(
    snapshot_id: str,
    role: Role = Depends(require_role(Role.SYSTEM_ADMIN))
):
    """
    Secondary JSON export pipeline for disaster recovery and offline replay.
    """
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(PlatformSnapshot).where(PlatformSnapshot.id == snapshot_id))
        snapshot = result.scalars().first()
        if not snapshot:
            return {"error": "Snapshot not found"}
            
        return {
            "snapshot_id": snapshot.id,
            "description": snapshot.description,
            "constitution_version": snapshot.constitution_version,
            "schema_epoch": snapshot.schema_epoch,
            "state_payload": snapshot.state_payload
        }
