from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from services.websocket_manager import manager

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        await manager.send(
            websocket,
            "Connected to DataVisionX Phoenix"
        )

        while True:
            await asyncio.sleep(30)

            try:
                await manager.send(websocket, "ping")
            except Exception:
                break

    except WebSocketDisconnect:
        pass

    finally:
        manager.disconnect(websocket)
