from core.runtime import runtime
from core.service import service
from core.plugins import plugin_manager


class HealthMonitor:

    def report(self):
        data = runtime.read()

        return {
            "status": data.get("status", "UNKNOWN"),
            "uptime": runtime.uptime(),
            "pid": service.read_pid(),
            "process": (
                "RUNNING"
                if service.is_running()
                else "STOPPED"
            ),
            "plugins": plugin_manager.count(),
        }


health = HealthMonitor()
