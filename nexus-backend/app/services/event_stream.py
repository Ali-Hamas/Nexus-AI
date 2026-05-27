import asyncio
from typing import Dict, Any
from app.events.bus import distributed_bus

class EventBusAdapter:
    async def publish(self, event_type: str, payload: Dict[str, Any]):
        # Route existing old events over the "events.raw" topic, or just use event_type as topic.
        # Since frontend expects SSE with type=event_type, we will just use event_type as topic.
        await distributed_bus.publish(event_type, payload)

    async def subscribe(self) -> asyncio.Queue:
        # Default subscribe for SSE is usually "watcher_feed" or all. Let's return watcher_feed.
        return await distributed_bus.subscribe("watcher_feed")

    def unsubscribe(self, queue: asyncio.Queue):
        distributed_bus.unsubscribe("watcher_feed", queue)

event_bus = EventBusAdapter()
