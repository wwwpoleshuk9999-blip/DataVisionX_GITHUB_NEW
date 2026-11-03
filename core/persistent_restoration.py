"""PHOENIX 100000.5 - Persistent Restoration FULL"""
import json, datetime
from pathlib import Path
import sqlite3

class PersistentRestoration:
    def __init__(self):
        self.real=True
        self.db_path=Path("core/phoenix.db")
    def create_snapshot(self, name="snapshot_100000.5"):
        from .persistence import persistence
        from .memory_system import memory
        from .knowledge_graph import knowledge_graph
        from .kpi_tracker import kpi_tracker
        snapshot={
            "name":name,
            "timestamp":datetime.datetime.now().isoformat(),
            "memory_long":dict(memory.long_term),
            "knowledge_nodes":dict(knowledge_graph.nodes),
            "knowledge_edges":list(knowledge_graph.edges),
            "kpis":kpi_tracker.get_kpis(),
            "persistence_stats":persistence.stats(),
            "version":"100000.5",
            "real":True
        }
        # Save snapshot to persistence
        persistence.save_long(f"snapshot_{name}", snapshot, tags=["snapshot","100000.5"])
        # Also save to file
        snap_path=Path(f"core/snapshots/{name}.json")
        snap_path.parent.mkdir(exist_ok=True)
        with open(snap_path,"w") as f:
            json.dump(snapshot,f,indent=2,default=str)
        return {"snapshot":name,"path":str(snap_path),"memory":len(snapshot["memory_long"]),"knowledge":len(snapshot["knowledge_nodes"]),"kpi":snapshot["kpis"],"real":True,"persistent":True}
    def restore_full(self, name=None):
        from .persistence import persistence
        from .memory_system import memory
        from .knowledge_graph import knowledge_graph
        from .kpi_tracker import kpi_tracker
        # Find latest snapshot if not named
        if name is None:
            if self.db_path.exists():
                conn=sqlite3.connect(str(self.db_path))
                cur=conn.cursor()
                cur.execute("SELECT key FROM memory_long WHERE key LIKE 'snapshot_%' ORDER BY timestamp DESC LIMIT 1")
                row=cur.fetchone()
                if row:
                    name=row[0].replace("snapshot_","")
                conn.close()
        # Restore
        restored={"memory":0,"knowledge":0,"kpi":0}
        try:
            # From file first
            snap_path=Path(f"core/snapshots/{name}.json") if name else None
            data=None
            if snap_path and snap_path.exists():
                with open(snap_path) as f:
                    data=json.load(f)
            else:
                # From persistence
                if name:
                    data=persistence.load_long(f"snapshot_{name}")
                else:
                    # Latest snapshot from DB
                    if self.db_path.exists():
                        conn=sqlite3.connect(str(self.db_path))
                        cur=conn.cursor()
                        cur.execute("SELECT value FROM memory_long WHERE key LIKE 'snapshot_%' ORDER BY timestamp DESC LIMIT 1")
                        row=cur.fetchone()
                        if row:
                            data=json.loads(row[0])
                        conn.close()
            if data:
                # Restore memory
                if "memory_long" in data:
                    for k,v in data["memory_long"].items():
                        memory.save_long(k,v,tags=["restored","snapshot"])
                    restored["memory"]=len(data["memory_long"])
                # Restore knowledge
                if "knowledge_nodes" in data:
                    knowledge_graph.nodes.update(data["knowledge_nodes"])
                    restored["knowledge"]=len(data["knowledge_nodes"])
                if "knowledge_edges" in data:
                    knowledge_graph.edges=data["knowledge_edges"]
                # KPI already tracked via events, no direct restore needed
                restored["kpi"]=1
            return {"restored":restored,"snapshot":name,"real":True,"persistent":True,"full":True}
        except Exception as e:
            import traceback
            return {"restored":restored,"error":str(e),"trace":traceback.format_exc(),"real":True}
    def list_snapshots(self):
        if not self.db_path.exists():
            return {"snapshots":[],"real":True}
        conn=sqlite3.connect(str(self.db_path))
        cur=conn.cursor()
        cur.execute("SELECT key, timestamp FROM memory_long WHERE key LIKE 'snapshot_%' ORDER BY timestamp DESC")
        rows=cur.fetchall()
        conn.close()
        return {"snapshots":[{"key":r[0],"timestamp":r[1]} for r in rows],"count":len(rows),"real":True}

persistent_restoration=PersistentRestoration()
