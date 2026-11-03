"""Phoenix 018 - AI Memory Agent - 100% REAL"""
import json, os
from datetime import datetime
from pathlib import Path

class Plugin:
    name = "AI Memory Agent"
    version = "1.0.0"
    
    def __init__(self):
        self.memory_file = Path("data/ai_memory.json")
        self.memory_file.parent.mkdir(exist_ok=True)
        self.memory = []
    
    def start(self):
        print(f"🧠 {self.name} v{self.version} starting...")
        self.load_memory()
        try:
            from plugin_manager.event_bus import event_bus
            event_bus.subscribe("ai_chat_request", self.on_chat)
            event_bus.subscribe("ai_memory_save", self.on_save)
        except:
            pass
        return f"{self.name} started - {len(self.memory)} memories"
    
    def stop(self):
        self.save_memory()
        return f"{self.name} stopped"
    
    def load_memory(self):
        try:
            if self.memory_file.exists():
                self.memory = json.loads(self.memory_file.read_text())[-100:]
        except:
            self.memory = []
    
    def save_memory(self):
        try:
            self.memory_file.write_text(json.dumps(self.memory[-100:], indent=2))
        except:
            pass
    
    def on_chat(self, data):
        query = data.get("query", "")
        if query:
            self.remember(query, "user_query")
    
    def on_save(self, data):
        self.remember(data.get("content", ""), data.get("type", "memory"))
    
    def remember(self, content: str, type_: str = "memory"):
        entry = {"content": content, "type": type_, "timestamp": datetime.now().isoformat()}
        self.memory.append(entry)
        self.memory = self.memory[-100:]
        self.save_memory()
        return entry
    
    def recall(self, query: str = "", limit: int = 10):
        if not query:
            return self.memory[-limit:]
        # Simple TF-IDF like search
        query_lower = query.lower()
        scored = []
        for m in self.memory:
            score = sum(1 for w in query_lower.split() if w in m["content"].lower())
            if score > 0:
                scored.append((score, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[:limit]]
    
    def get_stats(self):
        return {"total": len(self.memory), "types": list(set(m["type"] for m in self.memory)), "last": self.memory[-1] if self.memory else None}
