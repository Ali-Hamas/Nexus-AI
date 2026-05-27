import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import GraphEdge

async def apply_temporal_decay(session: AsyncSession):
    """
    Decays the relationship strength of edges over time.
    Edges that have not been updated recently lose strength.
    """
    now = datetime.datetime.utcnow()
    decay_rate_per_day = 0.05
    
    result = await session.execute(select(GraphEdge))
    edges = result.scalars().all()
    
    for edge in edges:
        days_old = (now - edge.last_updated_at).days
        if days_old > 0:
            decay_factor = days_old * decay_rate_per_day
            new_strength = max(0.1, edge.relationship_strength - decay_factor)
            
            if new_strength != edge.relationship_strength:
                edge.relationship_strength = new_strength
                
    await session.commit()
