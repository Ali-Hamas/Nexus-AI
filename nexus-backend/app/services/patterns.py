import datetime
from app.db.models import AsyncSessionLocal
from app.services.graph.entities import ensure_company_node, get_or_create_node
from app.services.graph.relationships import upsert_relationship

from enum import Enum

class ConvergencePattern(str, Enum):
    PRICING_CONVERGENCE = "PRICING_CONVERGENCE"
    AI_ACCELERATION = "AI_ACCELERATION"
    ENTERPRISE_EXPANSION = "ENTERPRISE_EXPANSION"
    FEATURE_PARITY_ESCALATION = "FEATURE_PARITY_ESCALATION"
    MARKET_CONSOLIDATION = "MARKET_CONSOLIDATION"
    PACKAGING_RESTRUCTURE = "PACKAGING_RESTRUCTURE"

class DivergencePattern(str, Enum):
    PRICING_DIVERGENCE = "PRICING_DIVERGENCE"
    ENTERPRISE_FRAGMENTATION = "ENTERPRISE_FRAGMENTATION"
    AI_POSITIONING_CONFLICT = "AI_POSITIONING_CONFLICT"
    MARKET_DECOUPLING = "MARKET_DECOUPLING"

class StrategicPatternEngine:
    async def classify_pattern(self, scenario: str, targets: list) -> str:
        # Deterministic heuristic mapping
        if "pricing" in scenario.lower():
            return ConvergencePattern.PRICING_CONVERGENCE.value
        if "ai" in scenario.lower():
            return ConvergencePattern.AI_ACCELERATION.value
        if "enterprise" in scenario.lower():
            return ConvergencePattern.ENTERPRISE_EXPANSION.value
        return ConvergencePattern.FEATURE_PARITY_ESCALATION.value

    async def record_convergence_cluster(self, sector: str, targets_involved: list, convergence_score: int, scenario: str = "pricing_change"):
        """
        Translates a temporal correlation event into persistent Strategic Memory in the Graph.
        """
        async with AsyncSessionLocal() as session:
            # 1. Ensure Sector Node
            sector_node = await get_or_create_node(
                session=session,
                node_type="Sector",
                name=sector,
                attributes={"type": "Market Sector"}
            )
            
            # 2. Create the Convergence Event Node
            pattern_type = await self.classify_pattern(scenario, targets_involved)
            cluster_name = f"{sector} {pattern_type}"
            cluster_node = await get_or_create_node(
                session=session,
                node_type="SectorTrend",
                name=cluster_name,
                sector=sector,
                attributes={
                    "last_score": convergence_score, 
                    "last_detected": datetime.datetime.utcnow().isoformat() + "Z",
                    "pattern_type": pattern_type
                }
            )
            
            # Link sector to trend
            await upsert_relationship(session, sector_node, cluster_node, "experiencing_trend", strength=0.9, confidence=100)
            
            # 3. Ensure Company Nodes and link them to the Convergence Cluster
            for target in targets_involved:
                comp_node = await ensure_company_node(session, target)
                
                # The company is part of the convergence cluster
                await upsert_relationship(session, comp_node, cluster_node, "driving_convergence", strength=0.8, confidence=convergence_score)
                
                # Also link the company to the Sector node directly for good graph structure
                await upsert_relationship(session, comp_node, sector_node, "belongs_to_sector", strength=1.0, confidence=100)
                
            # If multiple targets, draw lateral relationships between them
            if len(targets_involved) >= 2:
                for i in range(len(targets_involved)):
                    for j in range(i + 1, len(targets_involved)):
                        node_a = await ensure_company_node(session, targets_involved[i])
                        node_b = await ensure_company_node(session, targets_involved[j])
                        
                        await upsert_relationship(
                            session, 
                            node_a, 
                            node_b, 
                            "competing_with", 
                            strength=0.7 + (convergence_score / 1000.0), # Boost strength slightly based on recent clash
                            confidence=90
                        )

pattern_engine = StrategicPatternEngine()
