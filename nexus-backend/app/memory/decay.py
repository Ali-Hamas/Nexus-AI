import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.db.models import GraphEdge, GraphNode, AsyncSessionLocal
from app.events.bus import distributed_bus

logger = logging.getLogger(__name__)

class MemoryDecayEngine:
    """
    Living Cognition.
    Reinforcement-aware decay: Repeated convergence slows decay, silence accelerates it.
    """
    def __init__(self):
        self.BASE_DECAY_RATE = 0.05
        self.PRUNE_THRESHOLD = 0.1

    def _calculate_adaptive_decay(self, edge: GraphEdge, hours_since_update: float) -> float:
        # If confidence is high (reinforced many times), decay is slower
        confidence_factor = max(1, edge.confidence / 50.0) # e.g. 200 confidence = 4x slower decay
        
        # If it hasn't been updated in a long time (silence), decay accelerates
        silence_acceleration = 1.0 + (hours_since_update / 24.0)
        
        effective_decay = (self.BASE_DECAY_RATE / confidence_factor) * silence_acceleration
        return effective_decay

    async def run_decay_sweep(self):
        logger.info("Running Strategic Memory Decay Sweep...")
        now = datetime.datetime.utcnow()
        
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(GraphEdge))
            edges = result.scalars().all()
            
            decayed_count = 0
            pruned_count = 0
            
            for edge in edges:
                try:
                    last_update = datetime.datetime.fromisoformat(edge.last_updated_at.replace("Z", "+00:00")).replace(tzinfo=None)
                except Exception:
                    last_update = now
                    
                hours_since = (now - last_update).total_seconds() / 3600.0
                
                # Only decay if it hasn't been updated recently (e.g. > 1 hour)
                if hours_since > 1.0:
                    decay_amount = self._calculate_adaptive_decay(edge, hours_since)
                    edge.strength -= decay_amount
                    edge.last_updated_at = now.isoformat() + "Z"
                    decayed_count += 1
                    
                    if edge.strength < self.PRUNE_THRESHOLD:
                        await db.delete(edge)
                        pruned_count += 1
                        
                        await distributed_bus.publish("events.memory", {
                            "action": "PRUNE_EDGE",
                            "edge_id": edge.id,
                            "reason": "Decayed below viability threshold."
                        })
            
            await db.commit()
            
            # Prune orphan nodes (SectorTrends with no incoming edges)
            if pruned_count > 0:
                trend_result = await db.execute(select(GraphNode).where(GraphNode.node_type == "SectorTrend"))
                trends = trend_result.scalars().all()
                for t in trends:
                    # Check if it has any edges pointing to it
                    edges_to_trend = await db.execute(select(GraphEdge).where(GraphEdge.target_id == t.id))
                    if not edges_to_trend.scalars().first():
                        await db.delete(t)
                        await distributed_bus.publish("events.memory", {
                            "action": "PRUNE_NODE",
                            "node_id": t.id,
                            "reason": "Orphaned SectorTrend due to memory decay."
                        })
                await db.commit()
                
            logger.info(f"Decay Sweep Complete. Decayed {decayed_count} edges, Pruned {pruned_count} edges.")

decay_engine = MemoryDecayEngine()
