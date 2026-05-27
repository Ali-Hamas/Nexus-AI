from typing import Dict, Any, List

def compute_extraction_confidence(
    pricing_tiers: List[Dict[str, Any]], 
    features: List[str], 
    fingerprint: Dict[str, Any]
) -> int:
    """
    Deterministic confidence scoring engine.
    Returns a score from 0 to 100.
    """
    score = 0
    
    # 1. Pricing Tiers Found (+30)
    if len(pricing_tiers) > 0:
        score += 30
        
    # 2. Billing Cadence Found (+20)
    # Check if any pricing tier has a valid billing cadence
    has_billing = any(t.get("billing") for t in pricing_tiers)
    if has_billing:
        score += 20
        
    # 3. Feature Lists Matched (+20)
    if len(features) >= 3:
        score += 20
    elif len(features) > 0:
        score += 10
        
    # 4. DOM Consistency (+15)
    # If the structural fingerprint indicates a healthy page (has headings, lists, CTAs)
    if fingerprint.get("h2_count", 0) > 0 and fingerprint.get("list_count", 0) > 0 and fingerprint.get("cta_count", 0) > 0:
        score += 15
        
    # 5. Semantic Structure Valid (+15)
    # Are the pricing card candidates roughly matching the extracted tiers?
    candidates = fingerprint.get("pricing_card_candidates", 0)
    extracted_count = len(pricing_tiers)
    
    if candidates > 0 and extracted_count > 0:
        # If we extracted at least half of the potential candidates, the structure is solid
        if extracted_count >= (candidates / 2):
            score += 15
    elif candidates == 0 and extracted_count == 0:
        # If there are no candidates and we found nothing, it's structurally valid (just not a pricing page)
        # But we won't give it full points since we didn't extract data.
        pass
        
    # Cap at 100
    return min(score, 100)
