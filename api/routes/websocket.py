from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from services.websocket_manager import manager

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('WS REQUEST')
    await manager.connect(websocket)
    print('WS CONNECTED:', len(manager.connections))

    try:
        await manager.send(
            websocket,
            "Connected to DataVisionX Phoenix"
        )

        while True:
            await asyncio.sleep(30)

    except WebSocketDisconnect as e:
        print('WS CLIENT DISCONNECT:', e)

    finally:
        print('WS DISCONNECTED:', len(manager.connections))
        manager.disconnect(websocket)
