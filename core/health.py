from core.runtime import runtime
from core.service import service
from plugin_manager.manager import plugin_manager


class HealthMonitor:

    def report(self):

        running = service.is_running()

        if running:
            status = "RUNNING"
            runtime_status = runtime.read()["status"]
            pid = service.read_pid()
            uptime = runtime.uptime()
        else:
            status = "STOPPED"
            runtime_status = "STOPPED"
            pid = None
            uptime = 0

        return {
            "status": runtime_status,
            "uptime": uptime,
            "pid": pid,
            "process": status,
            "plugins": len(plugin_manager.list_plugins()),
        }


health = HealthMonitor()
