import os
import time
import shutil
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None


_history = []


class Metrics:

    def system(self):

        data = {
            "timestamp": int(time.time()),
            "uptime": time.time(),
        }

        if psutil:
            vm = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            data.update({
                "cpu_percent": psutil.cpu_percent(interval=0.2),
                "memory_total": vm.total,
                "memory_used": vm.used,
                "memory_percent": vm.percent,
                "disk_total": disk.total,
                "disk_used": disk.used,
                "disk_percent": disk.percent,
                "load_average": os.getloadavg() if hasattr(os, "getloadavg") else (0, 0, 0),
            })
        else:
            total, used, free = shutil.disk_usage("/")
            data.update({
                "cpu_percent": 0,
                "memory_total": 0,
                "memory_used": 0,
                "memory_percent": 0,
                "disk_total": total,
                "disk_used": used,
                "disk_percent": round(used / total * 100, 1),
                "load_average": (0, 0, 0),
            })

        
        _history.append(data)

        if len(_history) > 1000:
            _history.pop(0)

        return data



    def history(self):
        return list(_history)


metrics = Metrics()
