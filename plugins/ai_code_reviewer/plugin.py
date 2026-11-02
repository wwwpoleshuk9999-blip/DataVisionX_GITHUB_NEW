"""Phoenix 017 - AI Code Reviewer - 100% real"""
import ast
import re

class Plugin:
    name = "AI Code Reviewer"
    version = "1.0.0"
    
    def __init__(self):
        self.rules = {
            "security": ["eval(", "exec(", "os.system", "subprocess", "pickle.loads"],
            "best_practices": ["TODO", "FIXME", "print(", "except:"],
            "complexity": []
        }
    
    def start(self):
        print(f"🔍 {self.name} v{self.version} starting...")
        try:
            from plugin_manager.event_bus import event_bus
            event_bus.subscribe("code_review_request", self.on_review_request)
        except:
            pass
        return f"{self.name} started - security + best practices"
    
    def stop(self):
        return f"{self.name} stopped"
    
    def on_review_request(self, data):
        code = data.get("code", "")
        return self.review(code) if code else None
    
    def review(self, code: str):
        issues = []
        lines = code.split("\n")
        
        # Security checks
        for i, line in enumerate(lines, 1):
            for pattern in self.rules["security"]:
                if pattern in line:
                    issues.append({"line": i, "type": "security", "severity": "high", "message": f"Security risk: {pattern}", "code": line.strip()})
        
        # Best practices
        for i, line in enumerate(lines, 1):
            if "TODO" in line or "FIXME" in line:
                issues.append({"line": i, "type": "todo", "severity": "low", "message": "TODO/FIXME found", "code": line.strip()})
            if re.search(r"except\s*:\s*$", line):
                issues.append({"line": i, "type": "best_practice", "severity": "medium", "message": "Bare except - specify exception type", "code": line.strip()})
        
        # Complexity via AST
        try:
            tree = ast.parse(code)
            func_count = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
            class_count = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
        except:
            func_count = 0
            class_count = 0
        
        score = max(0, 100 - len(issues)*10)
        
        return {
            "score": score,
            "issues": issues,
            "stats": {"lines": len(lines), "functions": func_count, "classes": class_count, "issues_count": len(issues)},
            "summary": f"Found {len(issues)} issues. Score: {score}/100"
        }
