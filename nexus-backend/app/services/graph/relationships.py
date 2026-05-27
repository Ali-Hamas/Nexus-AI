from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import GraphEdge, GraphNode
import datetime

async def upsert_relationship(
    session: AsyncSession, 
    source_node: GraphNode, 
    target_node: GraphNode, 
    relation_type: str, 
    strength: float = 1.0, 
    confidence: int = 100
) -> GraphEdge:
    
    result = await session.execute(
        select(GraphEdge).where(
            GraphEdge.source_id == source_node.id,
            GraphEdge.target_id == target_node.id,
            GraphEdge.relationship_type == relation_type
        )
    )
    edge = result.scalars().first()
    
    if edge:
        # Boost strength if it already exists (reinforcement)
        edge.relationship_strength = min(1.0, edge.relationship_strength + (strength * 0.2))
        edge.confidence_score = max(edge.confidence_score, confidence)
        edge.last_updated_at = datetime.datetime.utcnow()
    else:
        edge = GraphEdge(
            source_id=source_node.id,
            target_id=target_node.id,
            relation_type=relation_type,
            relationship_strength=strength,
            confidence_score=confidence
        )
        session.add(edge)
        
    await session.commit()
    await session.refresh(edge)
    return edge
