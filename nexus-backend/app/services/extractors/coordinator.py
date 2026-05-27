from bs4 import BeautifulSoup
from typing import Dict, Any, Tuple
from app.services.extractors.pricing import extract_pricing_tiers
from app.services.extractors.features import extract_features
from app.services.extractors.structural import generate_structural_fingerprint
from app.services.extractors.confidence import compute_extraction_confidence

def execute_deterministic_extraction(html_content: str) -> Tuple[Dict[str, Any], int, Dict[str, Any]]:
    """
    Coordinates the deterministic extraction pipeline.
    Returns: (extracted_data, confidence_score, fingerprint)
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Structural Fingerprinting
    fingerprint = generate_structural_fingerprint(soup)
    
    # 2. Extract Data
    pricing_tiers = extract_pricing_tiers(soup)
    features = extract_features(soup)
    
    # 3. Compute Confidence
    confidence_score = compute_extraction_confidence(pricing_tiers, features, fingerprint)
    
    # 4. Assemble Final Data
    extracted_data = {
        "pricing": pricing_tiers,
        "features": features,
        "messaging": None,      # Reserved for LLM
        "release_notes": None,  # Reserved for LLM
        "timestamps": None      # Reserved for LLM
    }
    
    return extracted_data, confidence_score, fingerprint
