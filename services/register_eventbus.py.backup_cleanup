from core.event_bus import event_bus
from services.websocket_bridge import websocket_event_listener

event_bus.subscribe("START", websocket_event_listener)
event_bus.subscribe("STOP", websocket_event_listener)
event_bus.subscribe("RESTART", websocket_event_listener)

print("✅ EventBus -> WebSocket bridge registered")
