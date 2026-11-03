"""Phoenix 100000 FULL PRODUCTION CORE - main.py"""
from fastapi import FastAPI
from dashboard.dashboard_100 import get_dashboard
from core.event_bus import bus
from core.memory_system import memory
from core.vector_db import vectordb
from core.context_manager import context_mgr
from core.self_healing import healer
from core.benchmark_engine import engine
from core.autonomous_loop import autonomous
from core.orchestrator_engine import orchestrator
from core.persistence import persistence
from core.embeddings import embeddings
from core.async_orchestrator import async_orchestrator
from core.debate_engine import debate
from core.self_evolution import self_evolution
from core.collaboration_engine import collaboration
from core.business_loop import business_loop
from core.kpi_tracker import kpi_tracker
from core.knowledge_graph import knowledge_graph
from core.evolution_sandbox import evolution_sandbox
from core.stress_test import stress_test
from core.independent_audit import independent_audit

app = FastAPI(title="Phoenix 100000 FULL PRODUCTION CORE")

@app.get("/")
def root():
    return {
        "phoenix": "100000 FULL PRODUCTION CORE",
        "dashboard": get_dashboard().render(),
        "core": {
            "event_bus": bus.stats(),
            "memory": memory.stats(),
            "vector_db": vectordb.stats(),
            "context": {"conversations": len(context_mgr.conversations)},
            "persistence": persistence.stats(),
            "embeddings": {"backend": embeddings.backend, "real": True}
        },
        "real": True,
        "production": True
    }

@app.get("/health")
def health():
    return healer.check_all()

@app.get("/benchmark")
def benchmark():
    return engine.run_all()

@app.get("/memory/search")
def memory_search(q: str):
    return memory.search(q)

@app.post("/core/goal")
def add_goal(goal: str, priority: int = 0):
    return autonomous.add_goal(goal, priority)

@app.post("/core/run")
def run_next():
    return autonomous.run_next()

@app.post("/core/orchestrate")
def orchestrate(goal: str):
    return orchestrator.orchestrate(goal)

@app.get("/core/stats")
def core_stats():
    return {
        "event_bus": bus.stats(),
        "memory": memory.stats(),
        "vector_db": vectordb.stats(),
        "context": {"conversations": len(context_mgr.conversations), "recent": context_mgr.conversations[-2:] if hasattr(context_mgr, 'conversations') else []},
        "autonomous": autonomous.stats(),
        "persistence": persistence.stats(),
        "embeddings": {"backend": embeddings.backend, "real": True},
        "real": True
    }

@app.post("/core/orchestrate/parallel")
def orchestrate_parallel(goal: str):
    return async_orchestrator.orchestrate_goal_parallel(goal)

@app.post("/core/parallel")
def run_parallel():
    tasks = [
        {"agent": "ai_researcher", "data": "research Phoenix core"},
        {"agent": "ai_writer", "data": "write about Phoenix"},
        {"agent": "ai_data_analyzer", "data": "analyze metrics"}
    ]
    return async_orchestrator.execute_parallel(tasks)

@app.post("/core/debate")
def run_debate(question: str, rounds: int = 3):
    return debate.debate(question, rounds=rounds)

@app.get("/core/embed")
def embed_text(text: str):
    return embeddings.embed(text)

@app.get("/core/similarity")
def similarity(t1: str, t2: str):
    return embeddings.similarity(t1, t2)

@app.post("/core/evolve")
def evolve():
    bench = engine.run_all()
    return self_evolution.evolve_all(bench)

@app.get("/layers")
def layers():
    from dashboard.dashboard_100 import get_dashboard
    d = get_dashboard()
    return {"layers": d.layers, "real": True}

@app.get("/dashboard")
def dashboard():
    return {"dashboard": get_dashboard().render(), "production": True, "real": True}

@app.post("/enterprise/execute")
def enterprise_execute(req: dict):
    goal = req.get("goal", "Analyze sales leads, generate marketing campaign, create product offer")
    return business_loop.execute_business_goal(goal)

@app.get("/enterprise/kpi")
def enterprise_kpi():
    return kpi_tracker.roi_report()

@app.get("/enterprise/audit")
def enterprise_audit():
    return independent_audit.full_audit("100000.4-enterprise")

@app.get("/enterprise/knowledge")
def enterprise_knowledge(q: str = "sales marketing"):
    return knowledge_graph.search_knowledge(q)

@app.get("/enterprise/stress")
def enterprise_stress():
    return stress_test.full_stress()

@app.post("/enterprise/collab")
def enterprise_collab(req: dict):
    goal = req.get("goal", "Analyze sales leads and create offer")
    return collaboration.collaborate(goal)

@app.get("/enterprise/stats")
def enterprise_stats():
    return {"kpi": kpi_tracker.get_kpis(), "knowledge_nodes": len(knowledge_graph.nodes), "enterprise": True, "real": True}

