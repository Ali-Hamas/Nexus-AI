import asyncio
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.event_stream import event_bus

router = APIRouter()

@router.get("/stream")
async def event_stream():
    async def event_generator():
        queue = await event_bus.subscribe()
        try:
            while True:
                message = await queue.get()
                # Yield the payload directly for the frontend to consume
                yield f"data: {json.dumps(message['payload'])}\n\n"
        except asyncio.CancelledError:
            event_bus.unsubscribe(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
