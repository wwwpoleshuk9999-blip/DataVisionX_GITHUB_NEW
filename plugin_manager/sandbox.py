import os
from datetime import datetime


class PluginSandbox:

    def __init__(self, plugin_id, permission_manager):

        self.plugin_id = plugin_id
        self.permissions = permission_manager


    def log(self, message):

        os.makedirs(
            "runtime",
            exist_ok=True
        )

        with open(
            "runtime/plugins.log",
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"{datetime.now()} | "
                f"{self.plugin_id} | "
                f"{message}\n"
            )


    def request_event(self, event):

        if not self.permissions.require(
            self.plugin_id,
            "events"
        ):

            return False


        self.log(
            f"EVENT:{event}"
        )

        return True



    def storage_read(self, path):

        if not self.permissions.require(
            self.plugin_id,
            "storage"
        ):

            return None


        if not os.path.exists(path):
            return None


        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()



    def storage_write(self, path, data):

        if not self.permissions.require(
            self.plugin_id,
            "storage"
        ):

            return False


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(data)


        return True
