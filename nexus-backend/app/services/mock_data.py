import os
import json
from typing import Dict, Any

REPLAY_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "replay_snapshots")

def get_mock_snapshot(competitor: str, scenario: str) -> Dict[str, Any]:
    """
    Loads mock snapshot from the replay system.
    """
    filename = f"{competitor}_{scenario}_parsed_json.json"
    filepath = os.path.join(REPLAY_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_mock_diff(scenario: str, competitor: str = "Notion") -> Dict[str, Any]:
    """
    Loads and merges semantic diff and scoring output to represent a mock diff.
    """
    diff_filename = f"{competitor}_{scenario}_semantic_diff.json"
    score_filename = f"{competitor}_{scenario}_scoring_output.json"
    
    diff_filepath = os.path.join(REPLAY_DIR, diff_filename)
    score_filepath = os.path.join(REPLAY_DIR, score_filename)
    
    merged = {}
    if os.path.exists(diff_filepath):
        with open(diff_filepath, "r", encoding="utf-8") as f:
            merged.update(json.load(f))
            
    if os.path.exists(score_filepath):
        with open(score_filepath, "r", encoding="utf-8") as f:
            merged.update(json.load(f))
            
    return merged

def get_mock_governance_payload(competitor: str = "Notion", scenario: str = "pricing_change") -> Dict[str, Any]:
    """
    Loads mock governance payload.
    """
    filename = f"{competitor}_{scenario}_governance.json"
    filepath = os.path.join(REPLAY_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "reviewer": "admin",
        "action": "APPROVED",
        "timestamp": "2026-05-27T00:00:00Z",
        "notes": "Verified against competitor site. Legitimate pricing change."
    }
