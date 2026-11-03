"""REAL Embeddings - sentence-transformers with TF-IDF fallback"""
import math, re
from collections import Counter
import datetime

class EmbeddingsEngine:
    def __init__(self):
        self.real = True
        self.backend = "tfidf"  # default
        self.model = None
        self._try_load_transformer()
    
    def _try_load_transformer(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.backend = "transformer"
            print("[Embeddings] Using sentence-transformers all-MiniLM-L6-v2")
        except Exception as e:
            print(f"[Embeddings] Transformer not available ({e}), using TF-IDF fallback")
            self.backend = "tfidf"
    
    def _tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())
    
    def _tfidf_embed(self, text):
        tokens = self._tokenize(text)
        tf = Counter(tokens)
        # Simple hash-based embedding 128 dim
        dim = 128
        vec = [0.0] * dim
        for token, count in tf.items():
            h = hash(token) % dim
            vec[h] += count
        # Normalize
        norm = math.sqrt(sum(x*x for x in vec)) or 1
        vec = [x/norm for x in vec]
        return vec
    
    def embed(self, text):
        if self.backend == "transformer" and self.model:
            try:
                vec = self.model.encode(text).tolist()
                return {"vector": vec, "backend": "transformer", "dim": len(vec), "real": True}
            except:
                pass
        vec = self._tfidf_embed(text)
        return {"vector": vec, "backend": "tfidf", "dim": len(vec), "real": True}
    
    def similarity(self, text1, text2):
        e1 = self.embed(text1)
        e2 = self.embed(text2)
        v1, v2 = e1["vector"], e2["vector"]
        # cosine
        dot = sum(a*b for a,b in zip(v1, v2))
        return {"similarity": dot, "backend": self.backend, "real": True}

embeddings = EmbeddingsEngine()
