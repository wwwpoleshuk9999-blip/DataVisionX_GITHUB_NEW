"""PHOENIX 100000.7 - Persistent Ultimate - snapshot/restore full 100000.6+100000.7 state"""
import json, time, pathlib, sqlite3
from core.vector_memory_v2 import vector_memory_v2
from core.revenue_engine import revenue_engine

class PersistentUltimate:
    def __init__(self):
        self.db_path = pathlib.Path("core/phoenix_ultimate.db")
        self.snapshot_dir = pathlib.Path("core/snapshots_ultimate")
        self.snapshot_dir.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS ultimate_snapshots (id INTEGER PRIMARY KEY, version TEXT, data TEXT, timestamp REAL)")
        cur.execute("CREATE TABLE IF NOT EXISTS vector_docs (id TEXT PRIMARY KEY, text TEXT, meta TEXT, timestamp REAL)")
        conn.commit()
        conn.close()
    
    def snapshot_full(self, version="100000.7-enterprise-ultimate-plus"):
        from core.realtime_dashboard import realtime_dashboard
        from core.self_learning_loop import self_learning_loop
        from core.auto_scaling_engine import auto_scaling_engine
        
        data = {
            "version": version,
            "timestamp": time.time(),
            "dashboard": realtime_dashboard.full_realtime(),
            "revenue": revenue_engine.get_revenue_kpis(),
            "vector": vector_memory_v2.stats(),
            "learnings": self_learning_loop.get_learnings(10),
            "scaling": auto_scaling_engine.get_stats(),
            "real": True
        }
        
        # Save to file
        fname = self.snapshot_dir / f"ultimate_{version}_{int(time.time())}.json"
        fname.write_text(json.dumps(data, indent=2))
        
        # Save to DB
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO ultimate_snapshots (version, data, timestamp) VALUES (?,?,?)",
                    (version, json.dumps(data), time.time()))
        conn.commit()
        conn.close()
        
        return {
            "snapshot_file": str(fname),
            "version": version,
            "data_size": len(json.dumps(data)),
            "real": True,
            "persistent": True
        }
    
    def list_snapshots(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, version, timestamp FROM ultimate_snapshots ORDER BY timestamp DESC LIMIT 20")
        rows = cur.fetchall()
        conn.close()
        return {
            "total": len(rows),
            "snapshots": [{"id":r[0],"version":r[1],"timestamp":r[2]} for r in rows],
            "files": len(list(self.snapshot_dir.glob("*.json"))),
            "real": True
        }
    
    def restore_latest(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT data FROM ultimate_snapshots ORDER BY timestamp DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if row:
            data = json.loads(row[0])
            return {
                "restored": True,
                "version": data.get('version'),
                "timestamp": data.get('timestamp'),
                "data": data,
                "real": True
            }
        return {"restored": False, "reason": "no snapshot"}

persistent_ultimate = PersistentUltimate()
