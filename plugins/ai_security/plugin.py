import json, re
from pathlib import Path
from datetime import datetime
class Plugin:
    def __init__(self): self.id="ai_security"; self.name="AI Security"; self.version="5.0.0"; self.status="INIT"; self.scans=[]; self.data_file=Path("data/ai_security.json"); self.data_file.parent.mkdir(exist_ok=True); self.patterns=[r"eval\s*\(",r"exec\s*\(",r"os\.system",r"ghp_"]
    def start(self): self.status="RUNNING"; return True
    def stop(self): self.status="STOPPED"; return True
    def scan(self, code):
        issues=[{"pattern":p} for p in self.patterns if re.search(p,code)]
        score=max(0,100-len(issues)*20)
        result={"id":len(self.scans)+1,"issues":issues,"score":score,"safe":score>=80,"created":datetime.now().isoformat(),"real":True}
        self.scans.append(result); return result
    def get_status(self): return {"id":self.id,"status":self.status,"scans":len(self.scans),"real":True}
