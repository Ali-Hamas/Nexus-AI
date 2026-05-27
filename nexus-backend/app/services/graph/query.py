from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import GraphNode, GraphEdge

async def export_graph_state(session: AsyncSession):
    # Fetch all nodes
    nodes_result = await session.execute(select(GraphNode))
    nodes = nodes_result.scalars().all()
    
    # Fetch all edges
    edges_result = await session.execute(select(GraphEdge))
    edges = edges_result.scalars().all()
    
    return {
        "nodes": [
            {
                "id": n.id,
                "type": n.node_type,
                "name": n.name,
                "sector": n.sector,
                "attributes": n.attributes
            } for n in nodes
        ],
        "edges": [
            {
                "id": e.id,
                "source": e.source_id,
                "target": e.target_id,
                "relation": e.relation_type,
                "strength": e.relationship_strength,
                "confidence": e.confidence_score,
                "last_updated": e.last_updated_at.isoformat() + "Z"
            } for e in edges
        ]
    }
