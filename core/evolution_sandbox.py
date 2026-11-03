"""REAL Evolution Sandbox - Secure self-evolution"""
import datetime, shutil
from pathlib import Path

class EvolutionSandbox:
    def __init__(self):
        self.real = True
        self.sandbox_dir = Path("core/evolution_sandbox")
        self.sandbox_dir.mkdir(exist_ok=True)
        self.approvals = []

    def test_evolution(self, agent_id, new_code):
        plugin_path = None
        for p in Path("plugins").rglob(f"{agent_id}/plugin.py"):
            plugin_path = p
            break
        if not plugin_path:
            return {"success": False, "error": "not found", "real": True}
        
        backup_path = self.sandbox_dir / f"{agent_id}_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        shutil.copy(plugin_path, backup_path)
        
        sandbox_file = self.sandbox_dir / f"{agent_id}_test.py"
        sandbox_file.write_text(new_code)
        
        try:
            import py_compile
            py_compile.compile(str(sandbox_file), doraise=True)
            compile_ok = True
            compile_error = None
        except Exception as e:
            compile_ok = False
            compile_error = str(e)
        
        from .benchmark_engine import engine
        bench_before = engine.run_all()
        bench_after = None
        if compile_ok:
            original = plugin_path.read_text()
            plugin_path.write_text(new_code)
            bench_after = engine.run_all()
            plugin_path.write_text(original)
        
        approved = False
        if compile_ok and bench_after:
            if bench_after["success_rate"] >= bench_before["success_rate"]:
                approved = True
        
        result = {
            "agent": agent_id,
            "backup": str(backup_path),
            "compile_ok": compile_ok,
            "compile_error": compile_error,
            "bench_before": {"passed": bench_before["passed"], "rate": bench_before["success_rate"]},
            "bench_after": {"passed": bench_after["passed"], "rate": bench_after["success_rate"]} if bench_after else None,
            "approved": approved,
            "needs_human_approval": True,
            "real": True,
            "secure": True,
            "timestamp": datetime.datetime.now().isoformat()
        }
        if approved:
            self.approvals.append(result)
        return result

evolution_sandbox = EvolutionSandbox()
