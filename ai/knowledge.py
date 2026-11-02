import sqlite3, hashlib, math, re
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from typing import List, Dict

class AIKnowledge:
    """Phoenix 014 MAX: Vector TF-IDF + WAL + Cache + Versioning + External Safe"""
    def __init__(self, db_path="data/ai_knowledge.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
        self._cache = {}
        self._idf_cache = {}
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("""CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY, topic TEXT NOT NULL, content TEXT NOT NULL,
                source TEXT DEFAULT 'internal', content_hash TEXT, version INT DEFAULT 1,
                is_external INT DEFAULT 0, embedding TEXT, created_at TEXT, updated_at TEXT)""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_topic ON knowledge(topic)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_hash ON knowledge(content_hash)")
            conn.commit()
    
    def _now(self) -> str: return datetime.now(timezone.utc).isoformat()
    def _hash(self, c: str) -> str: return hashlib.sha256(c.encode()).hexdigest()[:16]
    def _sanitize(self, s: str) -> str: return (str(s)[:256].strip().replace("..","").replace(";","") or "internal") if s else "internal"
    def _tokenize(self, text: str) -> List[str]: return re.findall(r'\b\w{3,}\b', text.lower())
    def _tf(self, tokens: List[str]) -> Dict[str, float]:
        cnt=Counter(tokens); total=len(tokens); return {w: c/total for w,c in cnt.items()}
    def _idf(self, all_docs_tokens: List[List[str]]) -> Dict[str, float]:
        N=len(all_docs_tokens); df=Counter()
        for toks in all_docs_tokens:
            for w in set(toks): df[w]+=1
        return {w: math.log(N/(1+df[w]))+1 for w in df}
    def _vector(self, text: str, idf: Dict[str,float]) -> Dict[str,float]:
        toks=self._tokenize(text); tf=self._tf(toks)
        return {w: tf[w]*idf.get(w,1) for w in tf}
    def _cosine(self, v1: Dict[str,float], v2: Dict[str,float]) -> float:
        dot=sum(v1.get(k,0)*v2.get(k,0) for k in set(v1)|set(v2))
        norm1=math.sqrt(sum(x*x for x in v1.values())); norm2=math.sqrt(sum(x*x for x in v2.values()))
        return dot/(norm1*norm2) if norm1 and norm2 else 0
    
    def add(self, topic: str, content: str, source: str="internal") -> dict:
        if not topic or not content: return {"ok": False}
        topic=topic.strip()[:512]; content=content.strip(); chash=self._hash(content); source=self._sanitize(source); now=self._now()
        with sqlite3.connect(self.db_path) as conn:
            dup=conn.execute("SELECT id, version FROM knowledge WHERE topic=? AND content_hash=? ORDER BY version DESC LIMIT 1",(topic,chash)).fetchone()
            if dup: return {"ok": True, "id": dup[0], "version": dup[1], "duplicate": True}
            ver=(conn.execute("SELECT MAX(version) FROM knowledge WHERE topic=?",(topic,)).fetchone()[0] or 0)+1
            conn.execute("INSERT INTO knowledge (topic, content, source, content_hash, version, is_external, created_at, updated_at) VALUES (?,?,?,?,?,0,?,?)",(topic,content,source,chash,ver,now,now)); conn.commit()
            self._cache.clear(); self._idf_cache.clear()
            return {"ok": True, "version": ver}
    
    def add_external(self, topic: str, content: str, source: str) -> dict:
        if not source: return {"ok": False}
        topic=topic.strip()[:512]; content=content.strip()[:10000]; chash=self._hash(content); source=self._sanitize(source); now=self._now()
        with sqlite3.connect(self.db_path) as conn:
            dup=conn.execute("SELECT id FROM knowledge WHERE content_hash=? LIMIT 1",(chash,)).fetchone()
            if dup: return {"ok": True, "id": dup[0], "duplicate": True, "external": True}
            ver=(conn.execute("SELECT MAX(version) FROM knowledge WHERE topic=?",(topic,)).fetchone()[0] or 0)+1
            conn.execute("INSERT INTO knowledge (topic, content, source, content_hash, version, is_external, created_at, updated_at) VALUES (?,?,?,?,?,1,?,?)",(topic,content,source,chash,ver,now,now)); conn.commit()
            self._cache.clear(); self._idf_cache.clear()
            return {"ok": True, "version": ver, "external": True}
    
    def search(self, query: str, limit: int=20, include_external: bool=True) -> List[dict]:
        if not query or not query.strip(): return []
        query=query.strip()
        with sqlite3.connect(self.db_path) as conn:
            where_ext="" if include_external else "AND is_external=0"
            rows=conn.execute(f"SELECT topic, content, source, version, is_external, created_at, updated_at FROM knowledge WHERE 1=1 {where_ext} ORDER BY id DESC LIMIT 200").fetchall()
            if not rows: return []
            all_texts=[f"{r[0]} {r[1]}" for r in rows] + [query]
            all_tokens=[self._tokenize(t) for t in all_texts]
            idf=self._idf(all_tokens[:-1]) if len(all_tokens)>1 else {}
            q_vec=self._vector(query, idf)
            scored=[]
            for r in rows:
                doc_text=f"{r[0]} {r[1]}"
                d_vec=self._vector(doc_text, idf)
                cos=self._cosine(q_vec, d_vec)
                # bonus for exact token match
                tl=r[0].lower(); cl=r[1].lower(); bonus=0
                for tok in query.lower().split():
                    if len(tok)>2:
                        if tok in tl: bonus+=0.3
                        if tok in cl: bonus+=0.15
                score=cos+bonus+r[3]*0.01
                if score>0.05 or bonus>0:
                    scored.append((score,r))
            scored.sort(key=lambda x: x[0], reverse=True)
            return [{"topic": r[0], "content": r[1], "source": r[2], "version": r[3], "is_external": bool(r[4]), "created_at": r[5], "updated_at": r[6], "relevance": round(score,3)} for score,r in scored[:limit]]
    
    def list_topics(self) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            rows=conn.execute("SELECT topic, MAX(version), COUNT(*) FROM knowledge GROUP BY topic ORDER BY MAX(id) DESC").fetchall()
            return [{"topic": r[0], "latest_version": r[1], "count": r[2]} for r in rows]
