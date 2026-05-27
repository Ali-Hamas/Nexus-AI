from bs4 import BeautifulSoup
from typing import Dict, Any
import re

def generate_structural_fingerprint(soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Generates deterministic structural fingerprints for anomaly detection.
    """
    fingerprint = {
        "table_count": len(soup.find_all('table')),
        "h1_count": len(soup.find_all('h1')),
        "h2_count": len(soup.find_all('h2')),
        "h3_count": len(soup.find_all('h3')),
        "list_count": len(soup.find_all('ul')) + len(soup.find_all('ol')),
        "cta_count": 0,
        "pricing_card_candidates": 0
    }
    
    # Estimate CTA count (buttons or links with typical CTA text)
    cta_patterns = re.compile(r'(sign up|get started|try for free|contact sales|buy now)', re.IGNORECASE)
    buttons_and_links = soup.find_all(['button', 'a'])
    for element in buttons_and_links:
        if cta_patterns.search(element.get_text()):
            fingerprint["cta_count"] += 1
            
    # Estimate Pricing Card Candidates
    price_pattern = re.compile(r'\$\d+')
    potential_prices = soup.find_all(string=price_pattern)
    fingerprint["pricing_card_candidates"] = len(potential_prices)
    
    return fingerprint
