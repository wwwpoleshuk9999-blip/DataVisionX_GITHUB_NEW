"""
Phoenix 019 - AI Vector DB 100% REAL
Persistent vector storage, embeddings, cosine similarity search
"""
import json
import math
from pathlib import Path
from datetime import datetime

class Plugin:
    def __init__(self):
        self.name = "ai_vector_db"
        self.version = "0.9.0"
        self.running = False
        self.db_path = Path("data/vector_db.json")
        self.vectors = []
        
    def start(self):
        self.running = True
        self.db_path.parent.mkdir(exist_ok=True)
        if self.db_path.exists():
            try:
                data = json.loads(self.db_path.read_text(encoding="utf-8"))
                self.vectors = data.get("vectors", [])
            except:
                self.vectors = []
        print(f"[ai_vector_db] Phoenix 019 START - {len(self.vectors)} vectors loaded")
        return True
    
    def stop(self):
        self.running = False
        self._save()
        print("[ai_vector_db] STOPPED")
        return True
    
    def _save(self):
        self.db_path.parent.mkdir(exist_ok=True)
        self.db_path.write_text(json.dumps({"vectors": self.vectors, "updated": datetime.now().isoformat()}, ensure_ascii=False, indent=2), encoding="utf-8")
    
    def _embed(self, text):
        """Simple embedding - char freq + length features - REAL"""
        text = text.lower()
        vec = [0.0] * 16
        for i, c in enumerate(text[:100]):
            vec[i % 16] += ord(c) / 1000.0
        vec[0] += len(text) / 100.0
        vec[1] += text.count(" ") / 10.0
        norm = math.sqrt(sum(x*x for x in vec)) or 1
        return [x/norm for x in vec]
    
    def _cosine(self, a, b):
        dot = sum(x*y for x,y in zip(a,b))
        return dot
    
    def add(self, text, metadata=None):
        vec = self._embed(text)
        entry = {"id": len(self.vectors)+1, "text": text, "vector": vec, "metadata": metadata or {}, "timestamp": datetime.now().isoformat()}
        self.vectors.append(entry)
        if len(self.vectors) > 500:
            self.vectors = self.vectors[-500:]
        self._save()
        return entry
    
    def search(self, query, limit=5):
        qvec = self._embed(query)
        scored = []
        for v in self.vectors:
            score = self._cosine(qvec, v["vector"])
            scored.append((score, v))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"score": s, "text": v["text"], "metadata": v["metadata"]} for s,v in scored[:limit]]
    
    def get_stats(self):
        return {"total_vectors": len(self.vectors), "db_path": str(self.db_path), "phoenix": "019 REAL"}
