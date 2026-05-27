from typing import List, Dict, Any

# =========================================================================
# NEXUS - TARGET METADATA REGISTRY
# =========================================================================

TARGET_REGISTRY = {
    "Notion": {
        "sector": "Productivity SaaS",
        "company": "Notion",
        "priority": "HIGH",
        "monitoring_profile": "pricing+features",
        "region": "global",
        "risk_weight": 0.9,
        "interval_seconds": 30, # HIGH VOLATILITY TARGET
        "url": "https://www.notion.com/pricing"
    },
    "Airtable": {
        "sector": "Productivity SaaS",
        "company": "Airtable",
        "priority": "MEDIUM",
        "monitoring_profile": "pricing",
        "region": "global",
        "risk_weight": 0.7,
        "interval_seconds": 45,
        "url": "https://www.airtable.com/pricing"
    },
    "Monday": {
        "sector": "Productivity SaaS",
        "company": "Monday.com",
        "priority": "LOW",
        "monitoring_profile": "pricing",
        "region": "global",
        "risk_weight": 0.5,
        "interval_seconds": 60,
        "url": "https://monday.com/pricing"
    }
}

class TargetRegistryService:
    @staticmethod
    def get_all_targets() -> Dict[str, Dict[str, Any]]:
        return TARGET_REGISTRY
        
    @staticmethod
    def get_targets_by_sector(sector: str) -> Dict[str, Dict[str, Any]]:
        return {k: v for k, v in TARGET_REGISTRY.items() if v["sector"] == sector}

    @staticmethod
    def get_sectors() -> List[str]:
        return list(set(v["sector"] for v in TARGET_REGISTRY.values()))
