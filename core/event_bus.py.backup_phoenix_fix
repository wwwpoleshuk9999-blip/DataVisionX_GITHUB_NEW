from collections import defaultdict

class EventBus:
    def __init__(self):
        self._listeners = defaultdict(list)

    def subscribe(self, event_name, callback):
        self._listeners[event_name].append(callback)

    def publish(self, event_name, data=None):
        for callback in self._listeners.get(event_name, []):
            try:
                callback(data or {})
            except Exception as e:
                print(f"[EventBus] listener error: {e}")

    def emit(self, source, event_name, data=None):
        payload = {
            "source": source,
            "event": event_name,
            "data": data or {}
        }
        self.publish(event_name, payload)

event_bus = EventBus()
