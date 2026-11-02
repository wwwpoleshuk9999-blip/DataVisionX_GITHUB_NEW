import os
import copy
from datetime import datetime

EVENT_LOG = "runtime/events.log"

class EventBus:
    def __init__(self, permission_manager=None):
        self.permissions = permission_manager
        self.listeners = {}

    def _check_perm(self, plugin_id):
        if plugin_id == "system":
            return True
        if self.permissions is None:
            return True
        try:
            return self.permissions.require(plugin_id, "events")
        except:
            return True

    def register(self, plugin_id_or_event, event_or_callback=None, callback=None):
        # Поддержка обоих API:
        # Новый: register(plugin_id, event, callback)
        # Старый: subscribe(event, callback) -> plugin_id = "system"
        if callback is None:
            # Старый вызов: 2 аргумента
            event = plugin_id_or_event
            cb = event_or_callback
            plugin_id = "system"
        else:
            # Новый вызов: 3 аргумента
            plugin_id = plugin_id_or_event
            event = event_or_callback
            cb = callback

        if not callable(cb):
            return False
        if not self._check_perm(plugin_id):
            return False
        if event not in self.listeners:
            self.listeners[event] = []
        for listener in self.listeners[event]:
            if listener["plugin"] == plugin_id:
                return True
        self.listeners[event].append({
            "plugin": plugin_id,
            "callback": cb
        })
        self.log(f"{plugin_id} registered {event}")
        return True

    def unregister(self, plugin_id_or_event, event_or_callback=None, callback=None):
        if callback is None:
            event = plugin_id_or_event
            cb = event_or_callback
            plugin_id = "system"
        else:
            plugin_id = plugin_id_or_event
            event = event_or_callback
            cb = callback

        if not callable(cb):
            return False
        if not self._check_perm(plugin_id):
            return False
        listeners = self.listeners.get(event, [])
        for index, listener in enumerate(listeners):
            existing = listener["callback"]
            same_callback = existing is cb
            if (hasattr(existing, "__self__") and hasattr(existing, "__func__") and 
                hasattr(cb, "__self__") and hasattr(cb, "__func__")):
                same_callback = (existing.__self__ is cb.__self__ and existing.__func__ is cb.__func__)
            if listener["plugin"] == plugin_id and same_callback:
                del listeners[index]
                if not listeners:
                    self.listeners.pop(event, None)
                self.log(f"{plugin_id} unregistered {event}")
                return True
        return False

    def emit(self, plugin_id, event, data=None):
        # Тоже поддержка старого emit(event, data)
        if data is None and event is None:
            # emit(event, data) с plugin_id как event
            actual_event = plugin_id
            actual_data = None
            actual_plugin = "system"
        elif data is None and isinstance(event, dict):
            actual_event = plugin_id
            actual_data = event
            actual_plugin = "system"
        else:
            # Проверяем если вызвали emit(event, data) - 2 аргумента
            if isinstance(plugin_id, str) and isinstance(event, dict):
                actual_event = plugin_id
                actual_data = event
                actual_plugin = "system"
            else:
                actual_plugin = plugin_id
                actual_event = event
                actual_data = data

        if not self._check_perm(actual_plugin):
            return False
        self.log(f"{actual_plugin} emitted {actual_event}")
        listeners_snapshot = list(self.listeners.get(actual_event, []))
        for listener in listeners_snapshot:
            try:
                listener["callback"]({
                    "event": actual_event,
                    "source": actual_plugin,
                    "data": copy.deepcopy(actual_data)
                })
            except Exception as e:
                self.log(f"ERROR {listener['plugin']} {e}")
        return True

    def log(self, message):
        os.makedirs("runtime", exist_ok=True)
        with open(EVENT_LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} | {message}\n")

# LEGACY SINGLETON
event_bus = EventBus()
# ALIASES
EventBus.subscribe = EventBus.register
EventBus.unsubscribe = EventBus.unregister
