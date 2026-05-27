import json
import os
from typing import Dict, Any

REPLAY_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "replay_snapshots")

def save_replay(competitor: str, scenario: str, data_type: str, payload: Dict[str, Any]):
    """
    Saves payload to the replay system.
    data_type can be: raw_markdown, parsed_json, semantic_diff, scoring_output, governance, pdf_payload
    """
    if not os.path.exists(REPLAY_DIR):
        os.makedirs(REPLAY_DIR)
        
    filename = f"{competitor}_{scenario}_{data_type}.json"
    filepath = os.path.join(REPLAY_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

def load_replay(competitor: str, scenario: str, data_type: str) -> Dict[str, Any]:
    """
    Loads payload from the replay system for offline demo stability.
    """
    filename = f"{competitor}_{scenario}_{data_type}.json"
    filepath = os.path.join(REPLAY_DIR, filename)
    
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
