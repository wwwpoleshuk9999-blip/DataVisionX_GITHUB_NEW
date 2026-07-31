import time


class PluginHealthManager:

    def __init__(self):
        self.health = {}

    def register(self, plugin_id):

        if plugin_id not in self.health:
            self.health[plugin_id] = {
                "status": "UNKNOWN",
                "health": "UNKNOWN",
                "last_start": None,
                "restart_count": 0,
                "last_error": None
            }


    def started(self, plugin_id):

        self.register(plugin_id)

        self.health[plugin_id].update({
            "status": "RUNNING",
            "health": "OK",
            "last_start": int(time.time()),
            "last_error": None
        })


    def stopped(self, plugin_id):

        self.register(plugin_id)

        self.health[plugin_id].update({
            "status": "STOPPED",
            "health": "OK"
        })


    def failed(self, plugin_id, error):

        self.register(plugin_id)

        self.health[plugin_id].update({
            "status": "ERROR",
            "health": "FAILED",
            "last_error": str(error)
        })


    def recovered(self, plugin_id):

        self.register(plugin_id)

        self.health[plugin_id].update({
            "status": "RUNNING",
            "health": "RECOVERED",
            "restart_count":
                self.health[plugin_id]["restart_count"] + 1
        })


    def get(self, plugin_id):

        self.register(plugin_id)

        return self.health[plugin_id]


    def all(self):

        return self.health
