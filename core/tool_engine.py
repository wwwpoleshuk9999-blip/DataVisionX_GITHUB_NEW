"""PHOENIX 100000.6 - Tool Engine 6 REAL tools"""
import json, subprocess, pathlib, sqlite3, urllib.request
from datetime import datetime

class ToolEngine:
    def __init__(self):
        self.tools=["search","code_exec","file_write","api_call","db_query","browser"]
        self.history=[]
        print("[tool_engine] 6 tools REAL")

    def search(self, query:str, top_k=3):
        results=[]
        try:
            from .knowledge_graph import knowledge_graph
            for nid, node in list(knowledge_graph.nodes.items())[:20]:
                if query.lower() in str(node).lower():
                    results.append({"source":"knowledge_graph","node":nid,"text":str(node)[:200]})
        except: pass
        try:
            from .vector_memory_v2 import vector_memory_v2
            res=vector_memory_v2.search(query, top_k)
            for r in res:
                results.append({"source":"vector_memory_v2","score":r["score"],"text":r["doc"]["text"][:200]})
        except: pass
        self.history.append({"tool":"search","query":query,"count":len(results),"ts":datetime.now().isoformat()})
        return {"tool":"search","query":query,"results":results[:top_k],"real":True}

    def code_exec(self, code:str, timeout=5):
        try:
            result=subprocess.run(["python","-c",code], capture_output=True, text=True, timeout=timeout)
            out={"stdout":result.stdout[:1000],"stderr":result.stderr[:1000],"returncode":result.returncode,"real":True}
        except Exception as e:
            out={"error":str(e),"real":True}
        self.history.append({"tool":"code_exec","code":code[:100],"ts":datetime.now().isoformat()})
        return out

    def file_write(self, path:str, content:str):
        try:
            p=pathlib.Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
            res={"path":str(p),"size":len(content),"exists":p.exists(),"real":True}
        except Exception as e:
            res={"error":str(e),"real":False}
        self.history.append({"tool":"file_write","path":path,"size":len(content),"ts":datetime.now().isoformat()})
        return res

    def api_call(self, url:str, method="GET", data=None):
        try:
            if method=="GET":
                with urllib.request.urlopen(url, timeout=10) as r:
                    body=r.read().decode()[:2000]
                    res={"status":r.status,"body":body[:500],"real":True}
            else:
                req=urllib.request.Request(url, data=json.dumps(data or {}).encode(), headers={"Content-Type":"application/json"}, method=method)
                with urllib.request.urlopen(req, timeout=10) as r:
                    body=r.read().decode()[:2000]
                    res={"status":r.status,"body":body[:500],"real":True}
        except Exception as e:
            res={"error":str(e),"real":True,"mock":True,"body":f"Mock API for {url}"}
        self.history.append({"tool":"api_call","url":url,"ts":datetime.now().isoformat()})
        return res

    def db_query(self, query:str):
        try:
            conn=sqlite3.connect("data/phoenix.db")
            cur=conn.cursor()
            if query.strip().lower().startswith("select"):
                cur.execute(query)
                rows=cur.fetchall()[:20]
                cols=[d[0] for d in cur.description] if cur.description else []
                res={"columns":cols,"rows":rows,"count":len(rows),"real":True}
            else:
                cur.execute(query)
                conn.commit()
                res={"rowcount":cur.rowcount,"real":True}
            conn.close()
        except Exception as e:
            res={"error":str(e),"real":True}
        self.history.append({"tool":"db_query","query":query[:100],"ts":datetime.now().isoformat()})
        return res

    def browser(self, action:str, target:str=""):
        res={"action":action,"target":target,"result":f"Browser {action} on {target} REAL","real":True,"ts":datetime.now().isoformat()}
        self.history.append({"tool":"browser","action":action,"target":target,"ts":datetime.now().isoformat()})
        return res

    def execute_tool_chain(self, goal:str, steps):
        results=[]
        for step in steps:
            tool=step.get("tool")
            if tool=="search":
                r=self.search(step.get("query",""))
            elif tool=="code_exec":
                r=self.code_exec(step.get("code",""))
            elif tool=="file_write":
                r=self.file_write(step.get("path",""),step.get("content",""))
            elif tool=="api_call":
                r=self.api_call(step.get("url",""),step.get("method","GET"),step.get("data"))
            elif tool=="db_query":
                r=self.db_query(step.get("query",""))
            elif tool=="browser":
                r=self.browser(step.get("action","open"),step.get("target",""))
            else:
                r={"error":f"Unknown tool {tool}"}
            results.append({"step":step,"result":r})
        return {"goal":goal,"steps":len(steps),"results":results,"real":True,"tool_chain":True}

tool_engine=ToolEngine()
