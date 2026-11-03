"""REAL Persistence - SQLite Production Storage"""
import sqlite3, json, datetime
from pathlib import Path

class Persistence:
    def __init__(self, db_path="core/phoenix.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_db()
        self.real = True
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS memory_long 
                     (key TEXT PRIMARY KEY, value TEXT, tags TEXT, timestamp TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS memory_episodic 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, goal TEXT, steps TEXT, results TEXT, success INTEGER, timestamp TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS events 
                     (id TEXT PRIMARY KEY, type TEXT, data TEXT, source TEXT, timestamp TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS context_conversations 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT, metadata TEXT, timestamp TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS autonomous_goals 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, goal TEXT, priority INTEGER, status TEXT, result TEXT, added TEXT, completed TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS benchmark_results 
                     (agent_id TEXT, success INTEGER, response_time REAL, error TEXT, timestamp TEXT)""")
        conn.commit()
        conn.close()
    
    def save_long(self, key, value, tags=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO memory_long VALUES (?, ?, ?, ?)",
                  (key, json.dumps(value, ensure_ascii=False), json.dumps(tags or []), datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    
    def load_long(self, key):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT value, tags, timestamp FROM memory_long WHERE key=?", (key,))
        row = c.fetchone()
        conn.close()
        if row:
            return {"value": json.loads(row[0]), "tags": json.loads(row[1]), "timestamp": row[2], "real": True}
        return None
    
    def save_event(self, event):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO events VALUES (?, ?, ?, ?, ?)",
                  (event["id"], event["type"], json.dumps(event["data"], ensure_ascii=False), event["source"], event["timestamp"]))
        conn.commit()
        conn.close()
    
    def save_conversation(self, role, content, metadata=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO context_conversations VALUES (NULL, ?, ?, ?, ?)",
                  (role, content, json.dumps(metadata or {}), datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_recent_conversations(self, limit=20):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT role, content, timestamp FROM context_conversations ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        return [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in reversed(rows)]
    
    def stats(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        tables = ["memory_long", "memory_episodic", "events", "context_conversations", "autonomous_goals", "benchmark_results"]
        stats = {}
        for table in tables:
            try:
                c.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = c.fetchone()[0]
            except:
                stats[table] = 0
        conn.close()
        stats["real"] = True
        stats["db_path"] = str(self.db_path)
        return stats

persistence = Persistence()
