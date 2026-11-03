"""PHOENIX 100000.6 - Realtime Dashboard 200.0"""
from .enterprise_dashboard import enterprise_dashboard
from datetime import datetime

class RealtimeDashboard:
    def __init__(self):
        self.version="200.0 REALTIME ENTERPRISE ULTIMATE"
        self.streams=[]

    def full_realtime(self):
        base=enterprise_dashboard.full_dashboard()
        try:
            from .vector_memory_v2 import vector_memory_v2
            vm_stats=vector_memory_v2.stats()
        except:
            vm_stats={"total_docs":0,"dim":0,"backend":"unknown"}
        try:
            from .self_learning_loop import self_learning_loop
            learnings=self_learning_loop.get_learnings(5)
        except:
            learnings={"total":0}
        try:
            from .tool_engine import tool_engine
            tool_history=tool_engine.history[-10:]
            tools_count=len(tool_engine.history)
        except:
            tool_history=[]
            tools_count=0
        try:
            from .kpi_tracker import kpi_tracker
            kpi_live=kpi_tracker.get_kpis()
        except:
            kpi_live={}

        return {
            "version":self.version,
            "stable_base":base.get("stable_base","100000.5"),
            "timestamp":datetime.now().isoformat(),
            "base_dashboard":base,
            "vector_memory_v2":vm_stats,
            "learnings":learnings,
            "tool_engine":{"total_tools":6,"history_count":tools_count,"last_10":tool_history},
            "kpi_live":kpi_live,
            "realtime":True,
            "enterprise_ultimate":True,
            "websocket_ready":True
        }

    def stream_kpi(self):
        try:
            from .kpi_tracker import kpi_tracker
            kpi=kpi_tracker.get_kpis()
        except:
            kpi={}
        try:
            from .vector_memory_v2 import vector_memory_v2
            vdocs=vector_memory_v2.stats()["total_docs"]
        except:
            vdocs=0
        try:
            from .self_learning_loop import self_learning_loop
            learns=len(self_learning_loop.learnings)
        except:
            learns=0
        try:
            from .tool_engine import tool_engine
            tools=len(tool_engine.history)
        except:
            tools=0
        stream={"timestamp":datetime.now().isoformat(),"kpi":kpi,"vector_docs":vdocs,"learnings":learns,"tools_used":tools}
        self.streams.append(stream)
        return stream

realtime_dashboard=RealtimeDashboard()
