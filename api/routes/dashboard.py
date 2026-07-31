from fastapi import APIRouter
from core.plugin_registry import get_registry
import platform
import sys
import time

router = APIRouter(tags=["Dashboard"])

START_TIME = time.time()


@router.get("/dashboard/status")
def dashboard_status():

    plugins = {p["id"]: p for p in get_registry()}

    running = 0
    stopped = 0

    for plugin in plugins.values():

        if plugin.get("status") == "RUNNING":
            running += 1
        else:
            stopped += 1

    uptime = int(time.time() - START_TIME)

    return {

        "platform": "DataVisionX Phoenix",

        "version": "0.5 Beta",

        "status": "RUNNING",

        "health": "HEALTHY",

        "python": sys.version.split()[0],

        "os": platform.system(),

        "uptime_seconds": uptime,

        "plugins_total": len(plugins),

        "plugins_running": running,

        "plugins_stopped": stopped

    }
