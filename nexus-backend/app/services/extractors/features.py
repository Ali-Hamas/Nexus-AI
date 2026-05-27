from bs4 import BeautifulSoup
from typing import List

def extract_features(soup: BeautifulSoup) -> List[str]:
    """
    Extracts lists of features by analyzing DOM clusters, usually <ul>/<li> elements
    that are semantically close to pricing blocks, or standalone feature grids.
    """
    features = set()
    
    # Heuristic 1: Look for all <li> elements that contain a checkmark icon or text
    # that is reasonably short (a feature bullet).
    list_items = soup.find_all('li')
    
    for li in list_items:
        text = li.get_text(strip=True)
        # Features are usually short phrases, not paragraphs
        if 3 < len(text) < 80:
            # Check for generic noise (nav links, footer links)
            if li.find_parent('nav') or li.find_parent('footer'):
                continue
                
            # If the li has an SVG or img child, it's highly likely to be a feature checkmark
            if li.find(['svg', 'img']) or "✔" in text or "✓" in text:
                # Clean up tick marks from the text
                text = text.replace("✔", "").replace("✓", "").strip()
                features.add(text)
            else:
                # Still might be a feature if it's in a list that isn't a nav menu
                features.add(text)
                
    # Heuristic 2: Sometimes features are just stacked divs with a specific class or structure.
    # We can look for grids or rows.
    # We will stick to the safer <li> parsing for now to prevent noise.
    
    return list(features)
