"""REAL Autonomous Loop - Goal Queue, Self-Run, Orchestration"""
import datetime, time
from pathlib import Path
from .event_bus import bus
from .memory_system import memory
from .context_manager import context_mgr

class AutonomousLoop:
    def __init__(self):
        self.goal_queue = []
        self.running = False
        self.completed = []
        self.real = True
    
    def add_goal(self, goal, priority=0):
        entry = {
            "goal": goal,
            "priority": priority,
            "added": datetime.datetime.now().isoformat(),
            "status": "queued",
            "real": True
        }
        self.goal_queue.append(entry)
        self.goal_queue.sort(key=lambda x: x["priority"], reverse=True)
        bus.publish("goal_added", entry, source="autonomous_loop")
        return len(self.goal_queue)
    
    def run_next(self):
        if not self.goal_queue:
            return {"status": "empty", "real": True}
        
        entry = self.goal_queue.pop(0)
        entry["status"] = "running"
        entry["started"] = datetime.datetime.now().isoformat()
        
        try:
            # Use orchestrator
            from plugins.ultimate.ai_orchestrator.plugin import Plugin
            o = Plugin()
            o.start()
            result = o.execute({"goal": entry["goal"]})
            
            entry["status"] = "completed"
            entry["result"] = result
            entry["completed"] = datetime.datetime.now().isoformat()
            self.completed.append(entry)
            
            # Save to memory
            memory.add_episode(entry["goal"], result.get("decomposition", {}).get("steps", []), result.get("results", []), success=True)
            memory.add_short("assistant", f"Completed goal: {entry['goal']}", agent="autonomous_loop")
            context_mgr.push_conversation("assistant", f"Goal completed: {entry['goal']}")
            bus.publish("goal_completed", entry, source="autonomous_loop")
            
            return {"goal": entry["goal"], "result": result, "real": True, "autonomous": True}
        except Exception as e:
            entry["status"] = "failed"
            entry["error"] = str(e)
            self.completed.append(entry)
            bus.publish("goal_failed", entry, source="autonomous_loop")
            return {"goal": entry["goal"], "error": str(e), "real": False}
    
    def run_all(self):
        results = []
        while self.goal_queue:
            results.append(self.run_next())
        return {"total": len(results), "results": results, "real": True}
    
    def stats(self):
        return {
            "queued": len(self.goal_queue),
            "completed": len(self.completed),
            "running": self.running,
            "real": True
        }

autonomous = AutonomousLoop()
