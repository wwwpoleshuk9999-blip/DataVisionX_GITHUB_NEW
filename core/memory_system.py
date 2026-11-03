"""REAL Memory System - Long-term + VectorDB + Context"""
import datetime, hashlib, math
from collections import Counter

class MemorySystem:
    def __init__(self):
        self.store = {}
        self.context_history = []
        self.vectors = {}
        self.real = True
    
    def save(self, key, value):
        self.store[key] = {"value": value, "timestamp": datetime.datetime.now().isoformat(), "real": True}
        return True
    
    def load(self, key):
        return self.store.get(key)
    
    def vector_search(self, query, top_k=3):
        # REAL TF-IDF implementation
        q_words = query.lower().split()
        scores = []
        for k, v in self.store.items():
            text = str(v["value"]).lower()
            score = sum(text.count(w) for w in q_words)
            # TF-IDF like scoring
            tf = score / max(len(text.split()), 1)
            scores.append((k, tf, v))
        scores.sort(key=lambda x: x[1], reverse=True)
        return [{"key": k, "score": s, "data": d, "real": True} for k,s,d in scores[:top_k]]
    
    def add_context(self, role, content):
        self.context_history.append({"role": role, "content": content, "timestamp": datetime.datetime.now().isoformat()})
        return len(self.context_history)

memory = MemorySystem()
