"""REAL Knowledge Graph"""
import datetime, json
from pathlib import Path
import sqlite3

class KnowledgeGraph:
    def __init__(self):
        self.real=True
        self.nodes={}
        self.edges=[]
    def add_knowledge(self, key, value, relations=None):
        from .memory_system import memory
        from .vector_db import vectordb
        from .persistence import persistence
        self.nodes[key]={"value":value,"relations":relations or [],"timestamp":datetime.datetime.now().isoformat()}
        memory.save_long(key,value,tags=["knowledge_graph"])
        vectordb.add(key,str(value))
        persistence.save_long(key,value,tags=["knowledge_graph"])
        if relations:
            for rel in relations:
                self.edges.append({"from":key,"to":rel})
        return {"key":key,"nodes":len(self.nodes),"real":True}
    def search_knowledge(self, query, limit=5):
        from .vector_db import vectordb
        from .memory_system import memory
        vec=vectordb.search(query)
        mem=memory.search(query)
        related=[{"id":nid,"value":nd["value"]} for nid,nd in self.nodes.items() if query.lower() in str(nd["value"]).lower()][:limit]
        return {"query":query,"vector_results":vec[:limit],"memory_results":mem,"graph_results":related,"total_nodes":len(self.nodes),"total_edges":len(self.edges),"real":True,"persistent":True}
    def restore_from_persistence(self):
        from .persistence import persistence
        stats=persistence.stats()
        try:
            db_path=Path("core/phoenix.db")
            if not db_path.exists():
                db_path=Path("phoenix.db")
            restored=0
            if db_path.exists():
                conn=sqlite3.connect(str(db_path))
                cursor=conn.cursor()
                cursor.execute("SELECT key, value FROM memory_long ORDER BY timestamp DESC LIMIT 100")
                rows=cursor.fetchall()
                for key, val in rows:
                    try:
                        data=json.loads(val) if isinstance(val, str) else val
                        self.nodes[key]={"value":data,"relations":[],"timestamp":""}
                        restored+=1
                    except Exception as e:
                        self.nodes[key]={"value":val,"relations":[],"timestamp":""}
                        restored+=1
                conn.close()
            return {"restored":restored,"persistence_stats":stats,"db_exists":db_path.exists(),"db_path":str(db_path),"real":True,"persistent":True}
        except Exception as e:
            import traceback
            return {"restored":0,"persistence_stats":stats,"error":str(e),"trace":traceback.format_exc(),"real":True}

knowledge_graph=KnowledgeGraph()
