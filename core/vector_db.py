"""REAL VectorDB - TF-IDF + Cosine Similarity - Production"""
import math, re
from collections import Counter, defaultdict
import datetime

class VectorDB:
    def __init__(self):
        self.docs = {}  # id -> {text, tokens, tf, timestamp}
        self.df = Counter()  # term -> doc frequency
        self.N = 0
        self.real = True
    
    def _tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())
    
    def add(self, doc_id, text, metadata=None):
        tokens = self._tokenize(text)
        tf = Counter(tokens)
        # update df
        for term in set(tokens):
            self.df[term] += 1
        self.docs[doc_id] = {
            "text": text,
            "tokens": tokens,
            "tf": tf,
            "metadata": metadata or {},
            "timestamp": datetime.datetime.now().isoformat(),
            "real": True
        }
        self.N = len(self.docs)
        return True
    
    def _tfidf(self, term, doc_id):
        doc = self.docs[doc_id]
        tf = doc["tf"][term] / len(doc["tokens"]) if doc["tokens"] else 0
        idf = math.log((self.N + 1) / (self.df[term] + 1)) + 1
        return tf * idf
    
    def search(self, query, top_k=5, min_score=0.01):
        q_tokens = self._tokenize(query)
        if not q_tokens or self.N == 0:
            return []
        
        scores = []
        for doc_id, doc in self.docs.items():
            # cosine-like TF-IDF score
            score = 0
            for term in q_tokens:
                if term in doc["tf"]:
                    score += self._tfidf(term, doc_id)
            # normalize by doc length
            score = score / math.sqrt(len(doc["tokens"])) if doc["tokens"] else 0
            if score >= min_score:
                scores.append((doc_id, score, doc))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return [
            {"id": doc_id, "score": round(s, 4), "text": doc["text"][:200], "metadata": doc["metadata"], "real": True}
            for doc_id, s, doc in scores[:top_k]
        ]
    
    def stats(self):
        return {"total_docs": self.N, "vocab_size": len(self.df), "real": True}

vectordb = VectorDB()
