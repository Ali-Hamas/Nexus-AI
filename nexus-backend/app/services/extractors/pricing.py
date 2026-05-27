import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any

def extract_pricing_tiers(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    Extracts pricing tiers using resilient semantic heuristics (text density, keyword proximity, recurring structural blocks).
    Avoids fragile CSS selectors.
    """
    tiers = []
    
    # 1. Identify potential pricing blocks by looking for currency symbols and billing cadences.
    # We look for text nodes containing $ followed by a number.
    price_pattern = re.compile(r'\$\d+(?:\.\d{2})?')
    cadence_pattern = re.compile(r'/(?:mo|month|yr|year)', re.IGNORECASE)
    
    # Heuristic: A pricing card usually has a heading (tier name), a price, and a billing cadence.
    # We'll look for structural blocks (divs or sections) that contain these semantic markers.
    
    # Find all elements that look like a price
    potential_prices = soup.find_all(string=price_pattern)
    
    seen_blocks = set()
    
    for price_str in potential_prices:
        # Find the nearest enclosing container (likely a pricing card)
        # We walk up until we find a container with a heading or a list, or we reach a certain depth.
        card = price_str.parent
        depth = 0
        while card and card.name not in ['body', 'html'] and depth < 5:
            # Check if this card contains a heading (h1-h6) or a strong tag (often used for tier names)
            headings = card.find_all(['h2', 'h3', 'h4', 'strong'])
            if headings:
                break
            card = card.parent
            depth += 1
            
        if not card or id(card) in seen_blocks:
            continue
            
        seen_blocks.add(id(card))
        
        # Extract Tier Name
        tier_name = "Unknown"
        headings = card.find_all(['h2', 'h3', 'h4'])
        if not headings:
             headings = card.find_all(['strong', 'h5'])
        if headings:
             tier_name = headings[0].get_text(strip=True)
             
        # Extract Exact Price
        price_match = price_pattern.search(card.get_text())
        price = price_match.group(0) if price_match else price_str.strip()
        
        # Extract Billing Cadence
        cadence_match = cadence_pattern.search(card.get_text())
        billing = cadence_match.group(0).replace('/', '').strip() if cadence_match else "mo"
        
        # Some basic normalization
        if billing.lower() in ['mo', 'month']:
            billing = "monthly"
        elif billing.lower() in ['yr', 'year']:
            billing = "annually"
            
        if len(tier_name) < 25:  # Avoid accidentally capturing huge text blocks as tier names
            tiers.append({
                "tier_name": tier_name,
                "price": price,
                "billing": billing
            })
            
    # Fallback for "Enterprise" or "Contact Us" tiers which might not have a $ sign
    # We search for headings containing "Enterprise" or "Custom"
    enterprise_headings = soup.find_all(lambda tag: tag.name in ['h2', 'h3', 'h4'] and tag.string and any(word in tag.string.lower() for word in ['enterprise', 'custom', 'contact us']))
    for heading in enterprise_headings:
        card = heading.parent
        if id(card) not in seen_blocks:
             seen_blocks.add(id(card))
             tiers.append({
                 "tier_name": heading.get_text(strip=True),
                 "price": "Contact Us",
                 "billing": None
             })
             
    return tiers
