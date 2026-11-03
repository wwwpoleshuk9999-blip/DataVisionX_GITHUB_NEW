"""REAL EventBus - Phoenix 100000 MODULAR - Production"""
import datetime, json, threading
from collections import defaultdict, deque
from pathlib import Path

class EventBus:
    def __init__(self, max_history=1000):
        self.listeners = defaultdict(list)
        self.history = deque(maxlen=max_history)
        self.lock = threading.Lock()
        self.real = True
        self.persistent_file = Path("core/event_log.jsonl")
        self.persistent_file.parent.mkdir(exist_ok=True)
    
    def subscribe(self, event_type, callback, priority=0):
        with self.lock:
            self.listeners[event_type].append({"cb": callback, "priority": priority})
            self.listeners[event_type].sort(key=lambda x: x["priority"], reverse=True)
        return True
    
    def publish(self, event_type, data, source="system"):
        event = {
            "id": f"{datetime.datetime.now().timestamp():.6f}",
            "type": event_type,
            "data": data,
            "source": source,
            "timestamp": datetime.datetime.now().isoformat(),
            "real": True
        }
        with self.lock:
            self.history.append(event)
            # persist
            try:
                with open(self.persistent_file, "a") as f:
                    f.write(json.dumps(event, ensure_ascii=False) + "\n")
            except:
                pass
        
        results = []
        for listener in self.listeners.get(event_type, []) + self.listeners.get("*", []):
            try:
                res = listener["cb"](event)
                results.append({"success": True, "result": res})
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        
        return {"event": event, "delivered": len(results), "results": results, "real": True}
    
    def get_history(self, event_type=None, limit=50):
        hist = list(self.history)
        if event_type:
            hist = [h for h in hist if h["type"] == event_type]
        return hist[-limit:]
    
    def stats(self):
        return {
            "total_events": len(self.history),
            "event_types": list(self.listeners.keys()),
            "listeners_count": sum(len(v) for v in self.listeners.values()),
            "real": True
        }

bus = EventBus()
