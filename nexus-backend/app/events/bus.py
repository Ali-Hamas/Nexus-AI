import asyncio
import logging
import os
from typing import Dict, Any, List
from pydantic import ValidationError
from app.schemas.intelligence import CanonicalIntelligenceEvent

logger = logging.getLogger(__name__)

STRICT_SCHEMA_MODE = os.getenv("STRICT_SCHEMA_MODE", "SOFT")

class DistributedEventBus:
    """
    Interface-first architecture for the Distributed Event Bus.
    Preserves horizontal scalability readiness without operational fragility.
    Currently backed by in-memory asyncio Queues, partitioned by topic.
    """
    def __init__(self):
        # topic -> list of queues
        self._topics: Dict[str, List[asyncio.Queue]] = {}

    def _ensure_topic(self, topic: str):
        if topic not in self._topics:
            self._topics[topic] = []

    async def publish(self, topic: str, payload: Dict[str, Any]):
        # Hybrid Schema Enforcement
        if topic in ["watcher_feed", "events.governance"]:
            try:
                # Attempt to parse
                CanonicalIntelligenceEvent(**payload)
            except ValidationError as e:
                if STRICT_SCHEMA_MODE == "HARD":
                    logger.error(f"SCHEMA REJECTED on {topic}: {e}")
                    return # Reject publish
                else:
                    logger.warning(f"SCHEMA WARNING on {topic}: Legacy payload detected. Soft continuing.")
        
        self._ensure_topic(topic)
        message = {
            "topic": topic,
            "payload": payload
        }
        for queue in self._topics[topic]:
            await queue.put(message)

    async def subscribe(self, topic: str) -> asyncio.Queue:
        self._ensure_topic(topic)
        queue = asyncio.Queue()
        self._topics[topic].append(queue)
        return queue

    def unsubscribe(self, topic: str, queue: asyncio.Queue):
        if topic in self._topics and queue in self._topics[topic]:
            self._topics[topic].remove(queue)

    async def ack(self, message_id: str):
        """
        Acknowledgment interface for future persistent message brokers (Kafka/Redis).
        """
        pass

# Global singleton event bus
distributed_bus = DistributedEventBus()
