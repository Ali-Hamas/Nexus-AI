import datetime
import uuid
from typing import Dict, Any, List
from app.services.event_stream import event_bus
from app.services.patterns import pattern_engine

class MarketCorrelator:
    def __init__(self):
        # Stores recent escalations per sector
        self.sector_memory: Dict[str, List[Dict[str, Any]]] = {}
        # Tracks cooldowns to prevent alert storms
        self.sector_cooldowns: Dict[str, datetime.datetime] = {}
        
        self.CONVERGENCE_WINDOW_HOURS = 24
        self.CORRELATION_MEMORY_DAYS = 7
        self.ESCALATION_COOLDOWN_HOURS = 2
        
    async def process_escalation(self, competitor: str, metadata: Dict[str, Any], scores: Dict[str, Any], diff: Dict[str, Any]):
        """
        Ingests a new signal from a specific target and evaluates it against the sector memory.
        """
        sector = metadata.get("sector", "Unknown")
        now = datetime.datetime.utcnow()
        
        if sector not in self.sector_memory:
            self.sector_memory[sector] = []
            
        # 1. Store event in Correlation Memory
        event_record = {
            "competitor": competitor,
            "timestamp": now,
            "scores": scores,
            "diff": diff
        }
        self.sector_memory[sector].append(event_record)
        
        # 2. Prune old memory (7 days)
        cutoff_7d = now - datetime.timedelta(days=self.CORRELATION_MEMORY_DAYS)
        self.sector_memory[sector] = [e for e in self.sector_memory[sector] if e["timestamp"] > cutoff_7d]
        
        # 3. Check Cooldown (2 hours)
        if sector in self.sector_cooldowns:
            if now < self.sector_cooldowns[sector]:
                return # Suppress duplicate convergence (volatility dampening)
                
        # 4. Evaluate Convergence within 24h window
        cutoff_24h = now - datetime.timedelta(hours=self.CONVERGENCE_WINDOW_HOURS)
        recent_events = [e for e in self.sector_memory[sector] if e["timestamp"] > cutoff_24h]
        
        # We need events from at least 2 distinct competitors to form a convergence
        distinct_competitors = set(e["competitor"] for e in recent_events)
        if len(distinct_competitors) < 2:
            return
            
        convergence_score = self._calculate_convergence(recent_events)
        
        if convergence_score >= 75:
            # 5. Emit STRATEGIC_MARKET_CONVERGENCE
            event_id = f"conv_{uuid.uuid4().hex[:8]}"
            await event_bus.publish("watcher_feed", {
                "state": "STRATEGIC_MARKET_CONVERGENCE",
                "competitor": "SECTOR: " + sector.upper(),
                "message": f"Sector convergence detected across {len(distinct_competitors)} targets. Score: {convergence_score}",
                "timestamp": now.isoformat() + "Z",
                "convergence_score": convergence_score,
                "event_id": event_id,
                "targets_involved": list(distinct_competitors)
            })
            
            # Engage Cooldown
            self.sector_cooldowns[sector] = now + datetime.timedelta(hours=self.ESCALATION_COOLDOWN_HOURS)
            
            # Form Strategic Memory in the Graph
            scenario = metadata.get("scenario", "pricing_change")
            await pattern_engine.record_convergence_cluster(sector, list(distinct_competitors), convergence_score, scenario)

    def _calculate_convergence(self, recent_events: List[Dict[str, Any]]) -> int:
        score = 0
        
        # Collect signals across the events
        has_pricing = any("pricing" in e["diff"].get("additions", {}) or "pricing" in e["diff"].get("removals", {}) for e in recent_events)
        has_features = any("features" in e["diff"].get("additions", {}) for e in recent_events)
        
        # Mock semantic signals (in a full system, these come from the inference metadata)
        # For the demo, we use basic heuristics on the diff content
        
        if has_pricing:
            score += 30 # pricing alignment
            
        if has_features:
            score += 15 # packaging restructure
            
        # If we see multiple events happening at the same time
        if len(recent_events) >= 3:
            score += 10 # release cadence clustering
            
        # Simulate advanced semantic correlation
        # E.g. If both Notion and Airtable escalated, they might be shifting enterprise or AI.
        distinct_comps = set(e["competitor"] for e in recent_events)
        if "Notion" in distinct_comps and "Airtable" in distinct_comps:
            score += 20 # AI positioning similarity
            
        return min(score, 100)

market_correlator = MarketCorrelator()
