from collections import defaultdict
from typing import Callable, Any


class EventBus:
    def __init__(self):
        self._events: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[[Any], None]):
        """Подписаться на событие."""
        self._events[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[[Any], None]):
        """Отписаться от события."""
        if callback in self._events[event_name]:
            self._events[event_name].remove(callback)

    def publish(self, event_name: str, data: Any = None):
        """Отправить событие всем подписчикам."""
        for callback in self._events[event_name]:
            try:
                callback(data)
            except Exception as e:
                print(f"EventBus error: {e}")

    def subscribers(self, event_name: str) -> int:
        """Количество подписчиков."""
        return len(self._events[event_name])


event_bus = EventBus()
