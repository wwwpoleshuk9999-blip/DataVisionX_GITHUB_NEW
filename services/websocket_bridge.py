from services.websocket_manager import manager
import asyncio
import json


MAIN_LOOP = None


def set_loop(loop):
    global MAIN_LOOP
    MAIN_LOOP = loop


def websocket_event_listener(data):
    print("WEBSOCKET EVENT:", data)
    """
    Bridge: EventBus -> WebSocket
    """

    message = json.dumps(
        data,
        ensure_ascii=False
    )

    try:
        if MAIN_LOOP:

            asyncio.run_coroutine_threadsafe(
                manager.broadcast(message),
                MAIN_LOOP
            )
        else:
            print("WEBSOCKET LOOP NOT READY")

    except Exception as e:
        print(
            f"WebSocket bridge error: {e}"
        )
