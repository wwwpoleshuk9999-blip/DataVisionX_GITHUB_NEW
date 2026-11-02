import sqlite3, hashlib
from pathlib import Path
from datetime import datetime, timezone
from functools import lru_cache

class AIKnowledge:
    """Phoenix 013: Versioned knowledge with relevance ranking, external safe, RAG-ready"""
    def __init__(self, db_path="data/ai_knowledge.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
        self._search_cache = {}
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("""CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT NOT NULL, content TEXT NOT NULL,
                source TEXT DEFAULT 'internal', content_hash TEXT, version INTEGER DEFAULT 1,
                is_external INTEGER DEFAULT 0, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_topic ON knowledge(topic)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_hash ON knowledge(content_hash)")
            conn.commit()
    
    def _now(self) -> str: return datetime.now(timezone.utc).isoformat()
    def _hash(self, c: str) -> str: return hashlib.sha256(c.encode('utf-8')).hexdigest()[:16]
    def _sanitize(self, s: str) -> str: return (str(s)[:256].strip().replace("..","").replace(";","") or "internal") if s else "internal"
    
    def add(self, topic: str, content: str, source: str = "internal") -> dict:
        if not topic or not content: return {"ok": False}
        topic=topic.strip()[:512]; content=content.strip(); chash=self._hash(content); source=self._sanitize(source); now=self._now()
        with sqlite3.connect(self.db_path) as conn:
            dup=conn.execute("SELECT id, version FROM knowledge WHERE topic=? AND content_hash=? ORDER BY version DESC LIMIT 1",(topic,chash)).fetchone()
            if dup: return {"ok": True, "id": dup[0], "version": dup[1], "duplicate": True}
            ver=(conn.execute("SELECT MAX(version) FROM knowledge WHERE topic=?",(topic,)).fetchone()[0] or 0)+1
            cur=conn.execute("INSERT INTO knowledge (topic, content, source, content_hash, version, is_external, created_at, updated_at) VALUES (?,?,?,?,?,0,?,?)",(topic,content,source,chash,ver,now,now)); conn.commit()
            self._search_cache.clear()
            return {"ok": True, "id": cur.lastrowid, "version": ver}
    
    def add_external(self, topic: str, content: str, source: str) -> dict:
        if not source: return {"ok": False, "error": "source required"}
        topic=topic.strip()[:512]; content=content.strip()[:10000]; chash=self._hash(content); source=self._sanitize(source); now=self._now()
        with sqlite3.connect(self.db_path) as conn:
            dup=conn.execute("SELECT id FROM knowledge WHERE content_hash=? LIMIT 1",(chash,)).fetchone()
            if dup: return {"ok": True, "id": dup[0], "duplicate": True, "external": True}
            ver=(conn.execute("SELECT MAX(version) FROM knowledge WHERE topic=?",(topic,)).fetchone()[0] or 0)+1
            cur=conn.execute("INSERT INTO knowledge (topic, content, source, content_hash, version, is_external, created_at, updated_at) VALUES (?,?,?,?,?,1,?,?)",(topic,content,source,chash,ver,now,now)); conn.commit()
            self._search_cache.clear()
            return {"ok": True, "id": cur.lastrowid, "version": ver, "external": True}
    
    def search(self, query: str, limit: int = 20, include_external: bool = True) -> list:
        if not query or not query.strip(): return []
        query=query.strip()
        tokens=[t.lower() for t in query.split() if len(t)>2] or [query.lower()]
        cache_key=f"{query}:{limit}:{include_external}"
        if cache_key in self._search_cache: return self._search_cache[cache_key][:limit]
        
        with sqlite3.connect(self.db_path) as conn:
            where_ext="" if include_external else "AND is_external=0"
            like_clauses=" OR ".join(["topic LIKE ? OR content LIKE ?" for _ in tokens])
            params=[]
            for tok in tokens: params.extend([f"%{tok}%", f"%{tok}%"])
            rows=conn.execute(f"SELECT topic, content, source, version, is_external, created_at, updated_at FROM knowledge WHERE ({like_clauses}) {where_ext} ORDER BY id DESC LIMIT 100", params).fetchall()
            scored=[]
            for r in rows:
                tl=r[0].lower(); cl=r[1].lower(); score=0
                if query.lower() in tl: score+=10
                if query.lower() in cl: score+=5
                for tok in tokens:
                    if tok in tl: score+=3
                    if tok in cl: score+=1
                score+=r[3]*0.1
                scored.append((score,r))
            scored.sort(key=lambda x: x[0], reverse=True)
            result=[{"topic": r[0], "content": r[1], "source": r[2], "version": r[3], "is_external": bool(r[4]), "created_at": r[5], "updated_at": r[6], "relevance": round(score,2)} for score,r in scored[:limit]]
            self._search_cache[cache_key]=result
            return result
    
    def list_topics(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            rows=conn.execute("SELECT topic, MAX(version), COUNT(*) FROM knowledge GROUP BY topic ORDER BY MAX(id) DESC").fetchall()
            return [{"topic": r[0], "latest_version": r[1], "count": r[2]} for r in rows]
