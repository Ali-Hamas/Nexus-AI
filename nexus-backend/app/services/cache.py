import json
from typing import Dict, Any, Optional

# =========================================================================
# NEXUS - IN-MEMORY DETERMINISTIC CACHE
# =========================================================================

_IN_MEMORY_CACHE: Dict[str, str] = {}

async def store_snapshot_cache(competitor_name: str, url_hash: str, payload: Dict[str, Any], ttl_seconds: int = 86400) -> bool:
    """
    Stores the fetched markdown or json payload in memory for deterministic fallback recovery.
    Key format: nexus:snapshot:cache:[competitor_name]:[url_hash]
    """
    try:
        key = f"nexus:snapshot:cache:{competitor_name}:{url_hash}"
        _IN_MEMORY_CACHE[key] = json.dumps(payload)
        return True
    except Exception as e:
        print(f"Memory Cache Store Error: {e}")
        return False

async def get_snapshot_cache(competitor_name: str, url_hash: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves the cached payload for FALLBACK recovery mode.
    """
    try:
        key = f"nexus:snapshot:cache:{competitor_name}:{url_hash}"
        data = _IN_MEMORY_CACHE.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"Memory Cache Retrieve Error: {e}")
        return None
