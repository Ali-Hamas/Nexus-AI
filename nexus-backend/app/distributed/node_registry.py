import uuid
import datetime
from typing import Dict, Any

class LogicalNodeRegistry:
    """
    Manages Logical Execution Partitions (e.g. NODE_SAAS, NODE_AI)
    This provides horizontal scalability readiness without actual multi-machine complexity.
    """
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        
    def register_node(self, partition_name: str, targets: list) -> str:
        node_id = f"node_{uuid.uuid4().hex[:8]}"
        self.nodes[node_id] = {
            "id": node_id,
            "partition": partition_name,
            "targets": targets,
            "status": "ONLINE",
            "last_heartbeat": datetime.datetime.utcnow().isoformat() + "Z"
        }
        return node_id
        
    def get_all_nodes(self):
        return list(self.nodes.values())

node_registry = LogicalNodeRegistry()
