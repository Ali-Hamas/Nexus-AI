class InstitutionalTrustEngine:
    """
    Evaluates trust and integrity of intelligence payloads via weighted degradation.
    """
    
    def calculate_integrity(self, 
                            confidence: float, 
                            evidence_density: int, 
                            lineage_depth: int, 
                            replayability: float,
                            governance_verified: bool = False) -> float:
        """
        Weighted degradation integrity scoring.
        Starts with high potential (base model confidence), but degrades rapidly if evidence is thin
        or lineage is shallow. Replayability acts as a multiplier.
        """
        base_score = confidence
        
        # Degradation 1: Evidence Density (Scale 0-5 anchors)
        density_factor = min(1.0, max(0.2, evidence_density / 5.0))
        
        # Degradation 2: Lineage Depth (Scale 0-3 hops)
        lineage_factor = min(1.0, max(0.5, (lineage_depth + 1) / 3.0))
        
        # Multiplier: Replayability (Deterministic Reconstruction)
        replay_multiplier = min(1.0, replayability / 100.0)
        
        # Calculate raw degraded score
        integrity = base_score * density_factor * lineage_factor * replay_multiplier
        
        # Institutional bump
        if governance_verified:
            integrity = min(100.0, integrity * 1.25)
            
        return round(integrity, 2)

trust_engine = InstitutionalTrustEngine()
