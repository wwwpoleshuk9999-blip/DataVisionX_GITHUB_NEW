"""REAL Knowledge Graph - Persistent knowledge from Memory + VectorDB"""
import datetime
from .memory_system import memory
from .vector_db import vectordb
from .persistence import persistence

class KnowledgeGraph:
    def __init__(self):
        self.real = True
        self.nodes = {}
        self.edges = []

    def add_knowledge(self, key, value, relations=None):
        self.nodes[key] = {"value": value, "relations": relations or [], "timestamp": datetime.datetime.now().isoformat()}
        memory.save_long(key, value, tags=["knowledge_graph"])
        vectordb.add(key, str(value))
        persistence.save_long(key, value, tags=["knowledge_graph"])
        
        if relations:
            for rel in relations:
                self.edges.append({"from": key, "to": rel, "type": "related"})
        
        return {"key": key, "nodes": len(self.nodes), "real": True}

    def search_knowledge(self, query, limit=5):
        # Search via VectorDB + Memory
        vec_results = vectordb.search(query)
        mem_results = memory.search(query)
        
        # Build graph context
        related = []
        for node_id, node_data in self.nodes.items():
            if query.lower() in str(node_data["value"]).lower() or query.lower() in node_id.lower():
                related.append({"id": node_id, "value": node_data["value"], "relations": node_data["relations"]})
        
        return {
            "query": query,
            "vector_results": vec_results[:limit],
            "memory_results": mem_results,
            "graph_results": related[:limit],
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "real": True,
            "persistent": True
        }

    def restore_from_persistence(self):
        stats = persistence.stats()
        # Restore recent conversations and memory
        recent = persistence.get_recent_conversations(limit=20)
        restored = 0
        for conv in recent:
            self.nodes[f"conv_{restored}"] = {"value": conv, "relations": [], "timestamp": conv["timestamp"]}
            restored += 1
        
        return {"restored": restored, "persistence_stats": stats, "real": True}

knowledge_graph = KnowledgeGraph()
