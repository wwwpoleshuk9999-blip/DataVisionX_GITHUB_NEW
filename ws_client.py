import asyncio
import websockets


async def main():
    async with websockets.connect(
        "ws://127.0.0.1:8000/ws"
    ) as ws:
        print("CONNECTED")

        while True:
            msg = await ws.recv()
            print("EVENT:", msg)


asyncio.run(main())
