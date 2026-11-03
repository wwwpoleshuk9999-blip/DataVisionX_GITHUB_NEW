"""Phoenix 100000 AUTONOMOUS MODULAR - FULL CORE"""
from fastapi import FastAPI
from pathlib import Path
import json

app = FastAPI(title="Phoenix 100000 AUTONOMOUS MODULAR FULL CORE", version="100.0.0")

# Wire core
from core.event_bus import bus
from core.memory_system import memory
from core.context_manager import context_mgr
from core.self_healing import healer
from core.benchmark_engine import engine as bench_engine
from core.evolution_engine import evolution
from core.autonomous_loop import autonomous
from core.orchestrator_engine import orchestrator
from core.vector_db import vectordb

bus.subscribe("goal_added", lambda e: print(f"[EventBus] Goal added: {e['data']['goal']}"))
bus.subscribe("orchestration_done", lambda e: print(f"[EventBus] Done: {e['data']['goal']}"))

@app.get("/")
def root():
    manifest = json.loads(Path("plugins/manifest.json").read_text())
    return {
        "phoenix": "100000 AUTONOMOUS MODULAR FULL CORE",
        "version": "100.0.0",
        "architecture": "MODULAR + FULL CORE",
        "core": {
            "event_bus": bus.stats(),
            "memory": memory.stats(),
            "autonomous": autonomous.stats(),
            "healing": healer.check_all()
        },
        "layers": manifest.get("layers", {}),
        "total_agents": manifest.get("total", 0),
        "real": True,
        "autonomous": True,
        "modular": True,
        "full_core": True
    }

@app.get("/core/stats")
def core_stats():
    return {
        "event_bus": bus.stats(),
        "memory": memory.stats(),
        "context": len(context_mgr.conversations),
        "autonomous": autonomous.stats(),
        "vector_db": vectordb.stats(),
        "real": True
    }

@app.post("/core/goal")
def add_goal(goal: dict):
    g = goal.get("goal", "")
    p = goal.get("priority", 0)
    q_len = autonomous.add_goal(g, p)
    return {"goal": g, "queued": q_len, "real": True}

@app.post("/core/run")
def run_autonomous():
    return autonomous.run_next()

@app.post("/core/orchestrate")
def orchestrate_goal(goal: dict):
    g = goal.get("goal", "")
    return orchestrator.orchestrate(g)

@app.get("/health")
def health():
    return healer.check_all()

@app.get("/benchmark")
def benchmark():
    return bench_engine.run_all()

@app.get("/memory/search")
def search_memory(q: str):
    return memory.search(q)

@app.get("/layers")
def layers():
    return json.loads(Path("plugins/manifest.json").read_text())
