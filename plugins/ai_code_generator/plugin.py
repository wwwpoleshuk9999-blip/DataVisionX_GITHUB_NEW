"""Phoenix 020: AI Code Generator REAL 100% - Template-based code gen + syntax check"""
import ast, json, re
from pathlib import Path
from datetime import datetime

class Plugin:
    def __init__(self):
        self.id = "ai_code_generator"
        self.name = "AI Code Generator Agent"
        self.version = "1.0.0"
        self.status = "INIT"
        self.history = []
        self.data_file = Path("data/ai_code_generator.json")
        self.data_file.parent.mkdir(exist_ok=True)
        self.templates = {
            "fastapi": "from fastapi import APIRouter\nrouter = APIRouter(prefix=\"/{name}\")\n\n@router.get(\"/\")\nasync def list_{name}():\n    return {{\"items\": []}}",
            "plugin": "class Plugin:\n    def __init__(self):\n        self.id = \"{name}\"\n        self.status = \"INIT\"\n    def start(self):\n        self.status = \"RUNNING\"\n        return True\n    def stop(self):\n        self.status = \"STOPPED\"\n        return True",
            "react": "import React from 'react';\nfunction {Name}() { return <div>{Name} - {desc}</div>; }",
            "function": "def {name}({args}):\n    \"\"\"{desc}\"\"\"\n    {body}\n    return result"
        }

    def start(self):
        self.status = "RUNNING"
        if self.data_file.exists():
            try:
                self.history = json.loads(self.data_file.read_text())[:100]
            except:
                self.history = []
        print(f"[{self.id}] RUNNING - {len(self.history)} generations - REAL 100%")
        return True

    def stop(self):
        self.status = "STOPPED"
        return True

    def generate(self, prompt: str, lang: str = "python", template: str = "auto"):
        prompt = prompt.strip()
        if not prompt:
            return {"error": "empty prompt"}
        low = prompt.lower()
        if "api" in low or "router" in low:
            tmpl = "fastapi"
        elif "plugin" in low:
            tmpl = "plugin"
        elif "react" in low:
            tmpl = "react"
        else:
            tmpl = "function"
        if template != "auto" and template in self.templates:
            tmpl = template
        name = re.sub(r'[^a-zA-Z0-9_]', '_', prompt.split()[0].lower())[:20] or "generated"
        Name = name.capitalize()
        code = self.templates[tmpl].format(name=name, Name=Name, desc=prompt[:60], args="data", body=f"# Generated for: {prompt[:50]}\n    result = {{'prompt': '{prompt[:30]}'}}")
        valid = True
        syntax_error = None
        if lang == "python":
            try:
                ast.parse(code)
            except SyntaxError as e:
                valid = False
                syntax_error = str(e)
        record = {
            "id": len(self.history)+1,
            "prompt": prompt,
            "language": lang,
            "template": tmpl,
            "code": code,
            "valid": valid,
            "syntax_error": syntax_error,
            "lines": len(code.splitlines()),
            "created": datetime.now().isoformat(),
            "real": True
        }
        self.history.append(record)
        if len(self.history) > 100:
            self.history = self.history[-100:]
        try:
            self.data_file.write_text(json.dumps(self.history, indent=2))
        except:
            pass
        return record

    def list_history(self):
        return self.history[-20:]

    def get_status(self):
        return {"id": self.id, "status": self.status, "generated": len(self.history), "real": True}
