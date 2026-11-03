"""REAL Memory System - Long-term, Short-term, Episodic, Semantic"""
import datetime, json
from pathlib import Path
from .vector_db import VectorDB

class MemorySystem:
    def __init__(self):
        self.long_term = {}  # key -> value with timestamp
        self.short_term = []  # recent interactions max 100
        self.episodic = []  # episodes
        self.semantic = VectorDB()  # semantic memory via vector DB
        self.max_short = 100
        self.real = True
        self.persist_file = Path("core/memory.json")
    
    def save_long(self, key, value, tags=None):
        self.long_term[key] = {
            "value": value,
            "tags": tags or [],
            "timestamp": datetime.datetime.now().isoformat(),
            "real": True
        }
        self.semantic.add(key, str(value), {"type": "long_term", "tags": tags})
        return True
    
    def load_long(self, key):
        return self.long_term.get(key)
    
    def add_short(self, role, content, agent=None):
        entry = {
            "role": role,
            "content": content,
            "agent": agent,
            "timestamp": datetime.datetime.now().isoformat(),
            "real": True
        }
        self.short_term.append(entry)
        if len(self.short_term) > self.max_short:
            self.short_term = self.short_term[-self.max_short:]
        return len(self.short_term)
    
    def add_episode(self, goal, steps, results, success=True):
        episode = {
            "goal": goal,
            "steps": steps,
            "results": results,
            "success": success,
            "timestamp": datetime.datetime.now().isoformat(),
            "real": True
        }
        self.episodic.append(episode)
        self.semantic.add(f"episode_{len(self.episodic)}", f"{goal} {' '.join([str(s) for s in steps])}", {"type": "episodic"})
        return len(self.episodic)
    
    def search(self, query, top_k=5):
        # search across long-term + semantic
        semantic_results = self.semantic.search(query, top_k=top_k)
        long_results = []
        q_low = query.lower()
        for k, v in self.long_term.items():
            if q_low in str(v["value"]).lower() or q_low in k.lower():
                long_results.append({"id": k, "type": "long_term", "data": v, "real": True})
        return {"semantic": semantic_results, "long_term": long_results[:top_k], "real": True}
    
    def get_context_window(self, limit=20):
        return self.short_term[-limit:]
    
    def stats(self):
        return {
            "long_term": len(self.long_term),
            "short_term": len(self.short_term),
            "episodic": len(self.episodic),
            "semantic_docs": self.semantic.stats()["total_docs"],
            "real": True
        }

memory = MemorySystem()
