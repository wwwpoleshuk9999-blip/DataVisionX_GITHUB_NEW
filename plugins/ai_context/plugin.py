"""
Phoenix 019 - AI Context 100% REAL
Context Window + Memory + Vector DB fusion
"""
import json
from pathlib import Path
from datetime import datetime

class Plugin:
    def __init__(self):
        self.name = "ai_context"
        self.version = "0.9.0"
        self.running = False
        self.context_path = Path("data/ai_context.json")
        self.context_window = []
        self.max_window = 20
        
    def start(self):
        self.running = True
        self.context_path.parent.mkdir(exist_ok=True)
        if self.context_path.exists():
            try:
                data = json.loads(self.context_path.read_text(encoding="utf-8"))
                self.context_window = data.get("window", [])
            except:
                self.context_window = []
        print(f"[ai_context] Phoenix 019 START - window {len(self.context_window)}/{self.max_window}")
        return True
    
    def stop(self):
        self.running = False
        self._save()
        return True
    
    def _save(self):
        self.context_path.parent.mkdir(exist_ok=True)
        self.context_path.write_text(json.dumps({"window": self.context_window[-self.max_window:], "updated": datetime.now().isoformat()}, ensure_ascii=False, indent=2), encoding="utf-8")
    
    def add_context(self, role, content, metadata=None):
        entry = {"role": role, "content": content, "metadata": metadata or {}, "timestamp": datetime.now().isoformat()}
        self.context_window.append(entry)
        if len(self.context_window) > self.max_window:
            self.context_window = self.context_window[-self.max_window:]
        self._save()
        # Also push to vector DB and memory
        try:
            from plugins.ai_vector_db.plugin import Plugin as VectorDB
            vdb = VectorDB()
            vdb.start()
            vdb.add(content, {"role": role, **(metadata or {})})
        except:
            pass
        try:
            from plugins.ai_memory.plugin import Plugin as Memory
            mem = Memory()
            mem.start()
            mem.remember(f"{role}: {content}", "context")
        except:
            pass
        return entry
    
    def get_context(self, limit=None):
        lim = limit or self.max_window
        return self.context_window[-lim:]
    
    def search_context(self, query, limit=5):
        # Search via vector DB
        try:
            from plugins.ai_vector_db.plugin import Plugin as VectorDB
            vdb = VectorDB()
            vdb.start()
            return vdb.search(query, limit)
        except Exception as e:
            # Fallback simple text search
            results = []
            for c in self.context_window:
                if query.lower() in c["content"].lower():
                    results.append({"score": 1.0, "text": c["content"], "metadata": c})
            return results[:limit]
    
    def build_prompt(self, query):
        ctx = self.get_context(5)
        context_str = "\n".join([f"{c['role']}: {c['content']}" for c in ctx])
        prompt = f"Context:\n{context_str}\n\nQuery: {query}\n\nAnswer with context:"
        return prompt
    
    def clear(self):
        self.context_window = []
        self._save()
        return True
    
    def get_stats(self):
        return {"window_size": len(self.context_window), "max_window": self.max_window, "phoenix": "019 REAL 100%"}
