"""REAL Orchestrator Engine - Uses Core Systems"""
from .event_bus import bus
from .memory_system import memory
from .context_manager import context_mgr
from .self_healing import healer
from pathlib import Path
import datetime

class OrchestratorEngine:
    def __init__(self):
        self.real = True
    
    def orchestrate(self, goal, use_memory=True, use_healing=True):
        # 1. Check health if needed
        if use_healing:
            health = healer.check_all()
            if health["health_rate"] < 0.8:
                bus.publish("health_warning", health, source="orchestrator_engine")
        
        # 2. Search memory for similar goals
        memory_hits = []
        if use_memory:
            memory_hits = memory.search(goal, top_k=3)
            context_mgr.push_task({"goal": goal, "memory_hits": memory_hits})
        
        # 3. Run orchestrator agent
        from plugins.ultimate.ai_orchestrator.plugin import Plugin
        o = Plugin()
        o.start()
        result = o.execute({"goal": goal})
        
        # 4. Save context and memory
        context_mgr.push_conversation("user", goal)
        context_mgr.push_conversation("assistant", f"Orchestrated {result.get('completed', 0)} steps for {goal}")
        memory.add_episode(goal, result.get("decomposition", {}).get("steps", []), result.get("results", []))
        memory.add_short("assistant", f"Orchestrated: {goal}")
        
        bus.publish("orchestration_done", {"goal": goal, "result": result}, source="orchestrator_engine")
        
        return {
            "goal": goal,
            "memory_hits": memory_hits,
            "orchestration": result,
            "context": context_mgr.get_full_context(),
            "real": True,
            "autonomous": True,
            "timestamp": datetime.datetime.now().isoformat()
        }

orchestrator = OrchestratorEngine()
