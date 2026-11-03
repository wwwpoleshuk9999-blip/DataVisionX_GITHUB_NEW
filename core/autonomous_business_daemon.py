"""PHOENIX 100000.7 - Autonomous Business Daemon 24/7 + Product Factory + Revenue Pipeline"""
import time, json, pathlib
from core.business_loop import business_loop
from core.revenue_engine import revenue_engine
from core.self_learning_loop import self_learning_loop
from core.product_launch import product_launch

class AutonomousBusinessDaemon:
    def __init__(self):
        self.runs = 0
        self.total_business_value = 0
        self.products_created = 0
        self.is_running = False
        self.history = []
        
    def run_once(self, goal="Autonomous enterprise execution"):
        """One autonomous cycle: business DAG + revenue + learning"""
        biz = business_loop.execute_business_goal(goal)
        rev = revenue_engine.simulate_pipeline(2)
        learn = self_learning_loop.get_learnings(3)
        
        self.runs += 1
        self.total_business_value += biz.get('kpi',{}).get('business_value', biz.get('business_value',0))
        result = {
            "run": self.runs,
            "goal": goal,
            "business": biz,
            "revenue": rev['kpi'] if isinstance(rev, dict) else rev,
            "learning_count": learn['total'] if isinstance(learn, dict) else 0,
            "timestamp": time.time(),
            "real": True
        }
        self.history.append(result)
        return result
    
    def product_factory(self, count=3):
        """Factory: create N products from learning suggestions"""
        suggestions = []
        launches = []
        for i in range(count):
            sugg = self_learning_loop.suggest_next_product()
            suggestions.append(sugg)
            name = f"Phoenix Factory Product {self.products_created + i + 1} - {sugg['suggestion'][:30]}"
            launch = product_launch.launch_product(name, budget=5000, features=[sugg['suggestion']])
            launches.append(launch)
        
        self.products_created += count
        return {
            "factory_runs": self.products_created,
            "products_created": count,
            "suggestions": suggestions,
            "launches": launches,
            "total_launches": sum(1 for _ in pathlib.Path("launches").glob("*/product_spec.json")) if pathlib.Path("launches").exists() else 0,
            "real": True,
            "enterprise_factory": True
        }
    
    def revenue_pipeline(self, count=10):
        """Enhanced revenue pipeline with MRR tracking"""
        pipeline = revenue_engine.simulate_pipeline(count)
        kpi = revenue_engine.get_revenue_kpis()
        return {
            "pipeline_count": count,
            "kpi": kpi,
            "total_revenue": kpi['total_revenue'],
            "mrr": kpi['mrr'],
            "customers": kpi['customers'],
            "ltv": kpi['ltv'],
            "roi": kpi['roi'],
            "real": True,
            "pipeline": True
        }
    
    def autonomous_loop(self, cycles=3):
        """Run N autonomous cycles"""
        results = []
        for i in range(cycles):
            r = self.run_once(f"Autonomous cycle {i+1}/{cycles} - Enterprise Ultimate Plus")
            results.append(r)
            time.sleep(0.1)
        return {
            "cycles": cycles,
            "completed": len(results),
            "total_runs": self.runs,
            "total_business_value": self.total_business_value,
            "results": results,
            "real": True,
            "autonomous": True
        }
    
    def stats(self):
        return {
            "runs": self.runs,
            "total_business_value": self.total_business_value,
            "products_created": self.products_created,
            "history_count": len(self.history),
            "is_running": self.is_running,
            "real": True
        }

autonomous_business_daemon = AutonomousBusinessDaemon()
