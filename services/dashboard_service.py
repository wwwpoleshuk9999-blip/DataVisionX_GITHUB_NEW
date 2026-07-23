from core.health import health
import shutil


def _system():
    total, used, free = shutil.disk_usage("/")

    return {
        "disk_total": total,
        "disk_used": used,
        "disk_free": free,
    }


def dashboard():
    health_data = health.report()

    return {
        "project": "DataVisionX",
        "version": "0.3.0",
        "status": health_data.get("status", "UNKNOWN"),
        "process": health_data.get("process", "UNKNOWN"),
        "uptime": health_data.get("uptime", 0),
        "pid": health_data.get("pid"),
        "plugins": health_data.get("plugins", 0),
        "system": _system(),
    }
