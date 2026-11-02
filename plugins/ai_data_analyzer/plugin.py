"""Phoenix 017 - AI Data Analyzer - 100% real"""
import csv
import json
import statistics
from io import StringIO

class Plugin:
    name = "AI Data Analyzer"
    version = "1.0.0"
    
    def start(self):
        print(f"📊 {self.name} v{self.version} starting...")
        try:
            from plugin_manager.event_bus import event_bus
            event_bus.subscribe("data_analyze_request", self.on_analyze_request)
        except:
            pass
        return f"{self.name} started - CSV + insights ready"
    
    def stop(self):
        return f"{self.name} stopped"
    
    def on_analyze_request(self, data):
        csv_data = data.get("csv", "")
        return self.analyze(csv_data) if csv_data else None
    
    def analyze(self, csv_content: str):
        try:
            reader = csv.DictReader(StringIO(csv_content))
            rows = list(reader)
            if not rows:
                return {"error": "Empty CSV"}
            
            columns = reader.fieldnames
            stats = {}
            
            # Numeric columns stats
            for col in columns:
                values = []
                for row in rows:
                    try:
                        val = float(row[col])
                        values.append(val)
                    except:
                        pass
                if values:
                    stats[col] = {
                        "type": "numeric",
                        "count": len(values),
                        "mean": round(statistics.mean(values), 2),
                        "median": round(statistics.median(values), 2),
                        "min": round(min(values), 2),
                        "max": round(max(values), 2),
                        "stdev": round(statistics.stdev(values), 2) if len(values) > 1 else 0
                    }
                else:
                    # Categorical
                    unique_vals = list(set([r[col] for r in rows if r[col]]))
                    stats[col] = {
                        "type": "categorical",
                        "count": len(rows),
                        "unique": len(unique_vals),
                        "top_values": unique_vals[:5]
                    }
            
            insights = []
            insights.append(f"Dataset: {len(rows)} rows, {len(columns)} columns")
            for col, s in stats.items():
                if s["type"] == "numeric":
                    insights.append(f"{col}: avg {s['mean']}, range {s['min']}-{s['max']}")
                else:
                    insights.append(f"{col}: {s['unique']} unique values")
            
            return {
                "rows": len(rows),
                "columns": columns,
                "stats": stats,
                "insights": insights,
                "sample": rows[:3]
            }
        except Exception as e:
            return {"error": str(e)}
