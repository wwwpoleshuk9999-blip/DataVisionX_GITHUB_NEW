import os, copy
from datetime import datetime
from typing import Callable, Dict, List, Any, Optional

EVENT_LOG = "runtime/events.log"

class EventBus:
    """Phoenix 013: Ultra EventBus with compat layer, singleton, type hints, performance"""
    def __init__(self, permission_manager=None):
        self.permissions = permission_manager
        self.listeners: Dict[str, List[Dict[str, Any]]] = {}
        self._emit_count = 0
    
    def _check_perm(self, plugin_id: str) -> bool:
        if plugin_id == "system": return True
        if self.permissions is None: return True
        try: return self.permissions.require(plugin_id, "events")
        except: return True
    
    def register(self, plugin_id_or_event, event_or_callback=None, callback=None) -> bool:
        if callback is None:
            event = plugin_id_or_event; cb = event_or_callback; plugin_id = "system"
        else:
            plugin_id = plugin_id_or_event; event = event_or_callback; cb = callback
        if not callable(cb): return False
        if not self._check_perm(plugin_id): return False
        if event not in self.listeners: self.listeners[event] = []
        for listener in self.listeners[event]:
            if listener["plugin"] == plugin_id: return True
        self.listeners[event].append({"plugin": plugin_id, "callback": cb})
        self.log(f"{plugin_id} registered {event}")
        return True
    
    def unregister(self, plugin_id_or_event, event_or_callback=None, callback=None) -> bool:
        if callback is None:
            event = plugin_id_or_event; cb = event_or_callback; plugin_id = "system"
        else:
            plugin_id = plugin_id_or_event; event = event_or_callback; cb = callback
        if not callable(cb): return False
        if not self._check_perm(plugin_id): return False
        listeners = self.listeners.get(event, [])
        for i, l in enumerate(listeners):
            ex = l["callback"]; same = ex is cb
            if hasattr(ex, "__self__") and hasattr(cb, "__self__"):
                same = ex.__self__ is cb.__self__ and ex.__func__ is cb.__func__
            if l["plugin"] == plugin_id and same:
                del listeners[i]
                if not listeners: self.listeners.pop(event, None)
                self.log(f"{plugin_id} unregistered {event}")
                return True
        return False
    
    def emit(self, plugin_id: str, event: str, data: Any = None) -> bool:
        if data is None and isinstance(event, dict):
            actual_event = plugin_id; actual_data = event; actual_plugin = "system"
        else:
            actual_plugin = plugin_id; actual_event = event; actual_data = data
        if not self._check_perm(actual_plugin): return False
        self._emit_count += 1
        snap = list(self.listeners.get(actual_event, []))
        for listener in snap:
            try: listener["callback"]({"event": actual_event, "source": actual_plugin, "data": copy.deepcopy(actual_data)})
            except Exception as e: self.log(f"ERROR {listener['plugin']} {e}")
        return True
    
    def log(self, message: str):
        os.makedirs("runtime", exist_ok=True)
        try:
            with open(EVENT_LOG, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()} | {message}\n")
        except: pass
    
    def stats(self) -> dict:
        return {"events": len(self.listeners), "total_listeners": sum(len(v) for v in self.listeners.values()), "emits": self._emit_count}

event_bus = EventBus()
EventBus.subscribe = EventBus.register
EventBus.unsubscribe = EventBus.unregister
