"""PHOENIX 100000.6 - Vector Memory V2 384-dim"""
import math, re, json, sqlite3
from collections import Counter
from pathlib import Path

class VectorMemoryV2:
    def __init__(self, dim=384, db_path="data/phoenix.db"):
        self.dim_tfidf=128
        self.dim=dim
        self.db_path=db_path
        self.vocab={}
        self.idf={}
        self.docs=[]
        self.vectors=[]
        self.backend="tfidf"
        self.model=None
        try:
            from sentence_transformers import SentenceTransformer
            self.model=SentenceTransformer('all-MiniLM-L6-v2')
            self.dim=384
            self.backend="transformer"
            print("[vector_memory_v2] REAL transformer 384-dim loaded")
        except Exception as e:
            print(f"[vector_memory_v2] fallback tfidf 128-dim: {e}")

    def _tfidf_embed(self, text:str):
        tokens=re.findall(r'\w+', text.lower())
        if not tokens:
            return [0.0]*self.dim_tfidf
        for t in tokens:
            if t not in self.vocab:
                self.vocab[t]=len(self.vocab)
        vec=[0.0]*self.dim_tfidf
        cnt=Counter(tokens)
        for tok,c in cnt.items():
            idx=self.vocab.get(tok,0)%self.dim_tfidf
            tf=c/len(tokens)
            vec[idx]+=tf
        norm=math.sqrt(sum(x*x for x in vec)) or 1.0
        return [x/norm for x in vec]

    def embed(self, text:str):
        if self.model:
            try:
                v=self.model.encode(text).tolist()
                norm=math.sqrt(sum(x*x for x in v)) or 1.0
                return [x/norm for x in v]
            except:
                pass
        return self._tfidf_embed(text)

    def add(self, text:str, meta=None):
        vec=self.embed(text)
        doc_id=len(self.docs)
        self.docs.append({"id":doc_id,"text":text,"meta":meta or {}})
        self.vectors.append(vec)
        return doc_id

    def search(self, query:str, top_k=5):
        qvec=self.embed(query)
        scores=[]
        for i,vec in enumerate(self.vectors):
            dim=min(len(qvec),len(vec))
            dot=sum(qvec[j]*vec[j] for j in range(dim))
            scores.append((dot,i))
        scores.sort(reverse=True)
        res=[]
        for score, idx in scores[:top_k]:
            res.append({"score":score,"doc":self.docs[idx],"vector_dim":len(self.vectors[idx])})
        return res

    def save_persistent(self, text_content, doc_id):
        try:
            import sqlite3
            conn=sqlite3.connect('core/phoenix_ultimate.db')
            cur=conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS vector_docs (id TEXT PRIMARY KEY, text TEXT, meta TEXT, timestamp REAL)')
            cur.execute('INSERT OR REPLACE INTO vector_docs VALUES (?,?,?,?)', (doc_id, text_content[:5000], '{}', __import__('time').time()))
            conn.commit()
            conn.close()
        except: pass

    def stats(self):
        return {"total_docs":len(self.docs),"dim":self.dim if self.vectors else 0,"backend":self.backend,"vocab_size":len(self.vocab)}

vector_memory_v2=VectorMemoryV2()
