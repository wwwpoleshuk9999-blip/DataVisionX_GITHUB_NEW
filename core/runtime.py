from core.service_registry import ServiceRegistry
from core.plugin_registry_manager import PluginRegistryManager
from core.plugin_registry_manager import PluginRegistryManager
import os
import json
import time
from pathlib import Path


class RuntimeManager:

    def __init__(self):
        self.registry = ServiceRegistry()
        self.plugin_registry = PluginRegistryManager()
        self.plugin_registry = PluginRegistryManager()

        self.base_dir = Path("runtime")
        self.base_dir.mkdir(exist_ok=True)

        self.state_file = self.base_dir / "state.json"

        if not self.state_file.exists():
            self._create_default_state()


    def register_service(self, name, service):
        self.registry.register(
            name,
            service
        )


    def get_service(self, name):
        return self.registry.get(name)



    def _create_default_state(self):

        data = {
            "status": "STOPPED",
            "started_at": None,
            "last_action": "INIT",
            "restart_count": 0
        }

        self._save(data)


    def _load(self):

        try:
            with open(self.state_file, "r") as f:
                data = json.load(f)

        except Exception:

            data = {}

        # миграция старых state.json
        defaults = {
            "status": "STOPPED",
            "started_at": None,
            "last_action": "INIT",
            "restart_count": 0
        }

        for key, value in defaults.items():

            if key not in data:
                data[key] = value

        return data


    def _save(self, data):

        with open(self.state_file, "w") as f:
            json.dump(
                data,
                f,
                indent=4
            )


    def read(self):

        return self._load()


    def start(self):

        data = self._load()

        data["status"] = "RUNNING"
        data["started_at"] = int(time.time())
        data["last_action"] = "START"

        self._save(data)

        return data


    def stop(self):

        data = self._load()

        data["status"] = "STOPPED"
        data["last_action"] = "STOP"

        self._save(data)

        return data


    def reload(self):

        data = self._load()

        data["status"] = "RUNNING"
        data["last_action"] = "RELOAD"

        # безопасный счётчик рестартов
        data["restart_count"] = data.get(
            "restart_count",
            0
        ) + 1


        if data.get("started_at") is None:
            data["started_at"] = int(time.time())


        self._save(data)

        return data


    def uptime(self):

        data = self._load()

        started = data.get("started_at")

        if not started:
            return 0


        return int(time.time() - started)



runtime = RuntimeManager()
