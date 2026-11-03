"""REAL Business Loop"""
import datetime, time
from .collaboration_engine import collaboration
from .kpi_tracker import kpi_tracker
from .debate_engine import debate
from .memory_system import memory
from .persistence import persistence

class BusinessLoop:
    def __init__(self):
        self.real = True
        self.cycles = 0
    def execute_business_goal(self, goal):
        start = time.time()
        collab = collaboration.collaborate(goal)
        debate_res = None
        if len(collab["results"]) > 1 or "campaign" in goal.lower() or "budget" in goal.lower():
            debate_res = debate.debate(f"Best for: {goal} results {list(collab['results'].keys())}", rounds=2)
        for nid, res in collab["results"].items():
            kpi_tracker.track(nid, res, res.get("elapsed_ms", 0))
        memory.save_long(f"biz_{self.cycles}", {"goal": goal, "collab": collab["executed"]}, tags=["business", "enterprise"])
        persistence.save_long(f"biz_{self.cycles}", {"goal": goal, "kpis": kpi_tracker.get_kpis()})
        elapsed = (time.time()-start)*1000
        self.cycles += 1
        return {
            "goal": goal,
            "cycle": self.cycles,
            "collaboration": collab,
            "debate": debate_res,
            "kpis": kpi_tracker.get_kpis(),
            "roi": kpi_tracker.roi_report(),
            "elapsed_ms": elapsed,
            "explanation": f"Executed {collab['executed']}/{collab['total_nodes']} DAG nodes edges {len(collab['dag']['edges'])}. Debate: {debate_res['consensus'][:80] if debate_res else 'no debate'}. Value: {kpi_tracker.get_kpis()['business_value']}",
            "result": f"Business {goal} -> {collab['executed']} nodes value {kpi_tracker.get_kpis()['business_value']} ROI {kpi_tracker.roi_report()['roi_estimate']}",
            "real": True,
            "enterprise": True,
            "timestamp": datetime.datetime.now().isoformat()
        }
    def run_cycle(self, goal):
        return self.execute_business_goal(goal)
business_loop = BusinessLoop()
