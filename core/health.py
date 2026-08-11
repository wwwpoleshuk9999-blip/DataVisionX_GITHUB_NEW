from core.runtime import runtime
from core.service import service
from plugin_manager.manager import plugin_manager


class HealthMonitor:

    def report(self):

        runtime_data = runtime.read()

        process_running = service.is_running()

        total_plugins = len(plugin_manager.list_plugins())

        running_plugins = 0

        try:
            for plugin in plugin_manager.list_plugins():
                status = getattr(plugin, "status", "").upper()
                if status == "RUNNING":
                    running_plugins += 1
        except Exception:
            running_plugins = 0

        runtime_status = runtime_data.get("status", "UNKNOWN")

        if process_running:
            status = "RUNNING"
            uptime = runtime.uptime()
        elif runtime_status == "RUNNING":
            status = "RECOVERY_REQUIRED"
            uptime = 0
        else:
            status = runtime_status
            uptime = 0

        return {
            "status": status,
            "uptime": uptime,
            "pid": service.read_pid(),
            "process": "RUNNING" if process_running else "STOPPED",
            "plugins": total_plugins,
            "plugins_running": running_plugins,
            "plugins_stopped": total_plugins - running_plugins,
            "last_action": runtime_data.get("last_action"),
            "restart_count": runtime_data.get("restart_count", 0),
        }


health = HealthMonitor()
