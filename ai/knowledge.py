import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timezone
class AIKnowledge:
    def __init__(self, db_path="data/ai_knowledge.db"):
        self.db_path = Path(db_path); self.db_path.parent.mkdir(parents=True, exist_ok=True); self.init_db()
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT NOT NULL, content TEXT NOT NULL, source TEXT DEFAULT 'internal', content_hash TEXT, version INTEGER DEFAULT 1, is_external INTEGER DEFAULT 0, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_topic ON knowledge(topic)"); conn.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_hash ON knowledge(content_hash)"); conn.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_version ON knowledge(topic, version)"); conn.commit()
    def _now(self): return datetime.now(timezone.utc).isoformat()
    def _hash(self, c): return hashlib.sha256(c.encode('utf-8')).hexdigest()[:16]
    def _sanitize_source(self, s): return (str(s)[:256].strip().replace("..","").replace(";","") or "internal") if s else "internal"
    def add(self, topic, content, source="internal"):
        if not topic or not content: return {"ok": False}
        topic=str(topic).strip()[:512]; content=str(content).strip(); chash=self._hash(content); source=self._sanitize_source(source); now=self._now()
        with sqlite3.connect(self.db_path) as conn:
            dup=conn.execute("SELECT id, version FROM knowledge WHERE topic=? AND content_hash=? ORDER BY version DESC LIMIT 1",(topic,chash)).fetchone()
            if dup: return {"ok": True, "id": dup[0], "version": dup[1], "duplicate": True}
            row=conn.execute("SELECT MAX(version) FROM knowledge WHERE topic=?",(topic,)).fetchone(); next_ver=(row[0] or 0)+1
            cur=conn.execute("INSERT INTO knowledge (topic, content, source, content_hash, version, is_external, created_at, updated_at) VALUES (?,?,?,?,?,0,?,?)",(topic,content,source,chash,next_ver,now,now)); conn.commit(); return {"ok": True, "id": cur.lastrowid, "version": next_ver}
    def add_external(self, topic, content, source):
        if not source: return {"ok": False}
        topic=str(topic).strip()[:512]; content=str(content).strip()[:10000].replace("\x00",""); chash=self._hash(content); source=self._sanitize_source(source); now=self._now()
        with sqlite3.connect(self.db_path) as conn:
            dup=conn.execute("SELECT id FROM knowledge WHERE content_hash=? LIMIT 1",(chash,)).fetchone()
            if dup: return {"ok": True, "id": dup[0], "duplicate": True, "external": True}
            row=conn.execute("SELECT MAX(version) FROM knowledge WHERE topic=?",(topic,)).fetchone(); next_ver=(row[0] or 0)+1
            cur=conn.execute("INSERT INTO knowledge (topic, content, source, content_hash, version, is_external, created_at, updated_at) VALUES (?,?,?,?,?,1,?,?)",(topic,content,source,chash,next_ver,now,now)); conn.commit(); return {"ok": True, "id": cur.lastrowid, "version": next_ver, "external": True}
    def get(self, topic, version=None):
        with sqlite3.connect(self.db_path) as conn:
            r=conn.execute("SELECT topic, content, source, version, is_external, created_at, updated_at FROM knowledge WHERE topic=? ORDER BY version DESC LIMIT 1",(topic,)).fetchone() if version is None else conn.execute("SELECT topic, content, source, version, is_external, created_at, updated_at FROM knowledge WHERE topic=? AND version=?",(topic,version)).fetchone()
            return None if not r else {"topic": r[0], "content": r[1], "source": r[2], "version": r[3], "is_external": bool(r[4]), "created_at": r[5], "updated_at": r[6]}
    def search(self, query, limit=20, include_external=True):
        if not query or not str(query).strip(): return []
        query=str(query).strip(); tokens=[t.lower() for t in query.split() if len(t)>1] or [query.lower()]
        with sqlite3.connect(self.db_path) as conn:
            where_ext="" if include_external else "AND is_external=0"
            rows=conn.execute(f"SELECT topic, content, source, version, is_external, created_at, updated_at FROM knowledge WHERE (topic LIKE ? OR content LIKE ?) {where_ext} ORDER BY id DESC LIMIT 100",(f"%{query}%",f"%{query}%")).fetchall()
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
            return [{"topic": r[0], "content": r[1], "source": r[2], "version": r[3], "is_external": bool(r[4]), "created_at": r[5], "updated_at": r[6], "relevance": round(score,2)} for score,r in scored[:limit]]
    def list_topics(self):
        with sqlite3.connect(self.db_path) as conn:
            rows=conn.execute("SELECT topic, MAX(version), COUNT(*) FROM knowledge GROUP BY topic ORDER BY MAX(id) DESC").fetchall()
            return [{"topic": r[0], "latest_version": r[1], "count": r[2]} for r in rows]
    def delete(self, topic, version=None):
        with sqlite3.connect(self.db_path) as conn:
            cur=conn.execute("DELETE FROM knowledge WHERE topic=?",(topic,)) if version is None else conn.execute("DELETE FROM knowledge WHERE topic=? AND version=?",(topic,version))
            conn.commit(); return {"deleted": cur.rowcount}
