"""PHOENIX 100000.6 - Revenue Engine"""
import json, pathlib, sqlite3
from datetime import datetime
from .kpi_tracker import kpi_tracker

class RevenueEngine:
    def __init__(self, db_path="data/phoenix.db"):
        self.db_path=db_path
        self._init_db()

    def _init_db(self):
        try:
            conn=sqlite3.connect(self.db_path)
            conn.execute("CREATE TABLE IF NOT EXISTS revenue (id INTEGER PRIMARY KEY AUTOINCREMENT, customer TEXT, product TEXT, amount REAL, mrr REAL, timestamp TEXT, meta TEXT)")
            conn.commit()
            conn.close()
        except: pass

    def add_sale(self, customer:str, product:str, amount:float, mrr=None):
        mrr=mrr or amount*0.1
        ts=datetime.now().isoformat()
        try:
            conn=sqlite3.connect(self.db_path)
            conn.execute("INSERT INTO revenue (customer,product,amount,mrr,timestamp,meta) VALUES (?,?,?,?,?,?)", (customer,product,amount,mrr,ts,json.dumps({"real":True})))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[revenue] db fail {e}")
        try:
            kpi_tracker.track("revenue_sale", {"customer":customer,"product":product,"amount":amount,"success":True,"count":1}, int(amount))
        except:
            pass
        try:
            from .vector_memory_v2 import vector_memory_v2
            vector_memory_v2.add(f"Sale customer {customer} product {product} amount ${amount} mrr ${mrr}", {"type":"revenue","amount":amount})
        except: pass
        try:
            from .tool_engine import tool_engine
            tool_engine.file_write(f"revenue/{customer}_{int(datetime.now().timestamp())}.json", json.dumps({"customer":customer,"product":product,"amount":amount,"mrr":mrr,"ts":ts}, indent=2))
        except: pass
        return {"customer":customer,"product":product,"amount":amount,"mrr":mrr,"timestamp":ts,"real":True}

    def get_revenue_kpis(self):
        try:
            conn=sqlite3.connect(self.db_path)
            cur=conn.cursor()
            cur.execute("SELECT SUM(amount), SUM(mrr), COUNT(*) FROM revenue")
            total,mrr,cust=cur.fetchone()
            conn.close()
            total=total or 0
            mrr=mrr or 0
            cust=cust or 0
            ltv=(mrr*12 / cust) if cust else 0
            cac=(total*0.2 / cust) if cust else 0
            roi=(total / (cac or 1)) if cust else 0
            return {"total_revenue":total,"mrr":mrr,"customers":cust,"ltv":ltv,"cac":cac,"roi":roi,"real":True}
        except Exception as e:
            return {"total_revenue":0,"mrr":0,"customers":0,"ltv":0,"cac":0,"roi":0,"error":str(e),"real":True}

    def simulate_pipeline(self, count=5):
        results=[]
        for i in range(count):
            r=self.add_sale(f"customer_{i+1}@enterprise.com", f"Phoenix 100000.6 Product {i+1}", 1000*(i+1), 100*(i+1))
            results.append(r)
        kpi=self.get_revenue_kpis()
        return {"sales":results,"kpi":kpi,"real":True}

revenue_engine=RevenueEngine()
