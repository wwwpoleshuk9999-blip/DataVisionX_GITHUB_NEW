import os
import json
import importlib
import traceback
import datetime

from plugin_manager.sandbox import PluginSandbox


PLUGINS_DIR = "plugins"
RUNTIME_FILE = "runtime/plugins.json"
LOG_FILE = "runtime/plugins.log"
SECURITY_LOG = "runtime/security.log"


class PermissionManager:

    def __init__(self, manager):
        self.manager = manager


    def check(self, plugin_id, permission):

        plugin = self.manager.plugins.get(
            plugin_id,
            {}
        )

        permissions = plugin.get(
            "permissions",
            {}
        )

        return permissions.get(
            permission,
            False
        )


    def require(self, plugin_id, permission):

        result = self.check(
            plugin_id,
            permission
        )

        if not result:
            self.audit(
                plugin_id,
                permission
            )

        return result


    def audit(self, plugin_id, permission):

        os.makedirs(
            "runtime",
            exist_ok=True
        )

        with open(
            SECURITY_LOG,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"{datetime.datetime.now()} | "
                f"{plugin_id} | "
                f"{permission} | BLOCKED\n"
            )



class PluginManager:

    def __init__(self):

        self.plugins = {}
        self.instances = {}
        self.sandboxes = {}

        self.permissions = PermissionManager(
            self
        )

        self.load_state()
        self.scan_plugins()
        self.auto_start()



    def log(self, message):

        os.makedirs(
            "runtime",
            exist_ok=True
        )

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                message + "\n"
            )



    def load_state(self):

        os.makedirs(
            "runtime",
            exist_ok=True
        )

        if os.path.exists(
            RUNTIME_FILE
        ):

            with open(
                RUNTIME_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                self.plugins = json.load(
                    f
                )



    def save_state(self):

        with open(
            RUNTIME_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.plugins,
                f,
                indent=4,
                ensure_ascii=False
            )



    def scan_plugins(self):

        os.makedirs(
            PLUGINS_DIR,
            exist_ok=True
        )

        for name in os.listdir(
            PLUGINS_DIR
        ):

            path = os.path.join(
                PLUGINS_DIR,
                name
            )

            if not os.path.isdir(path):
                continue


            manifest_path = os.path.join(
                path,
                "manifest.json"
            )

            if not os.path.exists(
                manifest_path
            ):
                continue


            with open(
                manifest_path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)


            if name not in self.plugins:

                self.plugins[name] = {

                    "name": data.get(
                        "name",
                        name
                    ),

                    "version": data.get(
                        "version",
                        "1.0"
                    ),

                    "description": data.get(
                        "description",
                        ""
                    ),

                    "permissions": data.get(
                        "permissions",
                        {}
                    ),

                    "status": "STOPPED"
                }

            else:

                self.plugins[name]["permissions"] = data.get(
                    "permissions",
                    {}
                )


        self.save_state()



    def list_plugins(self):

        return list(
            self.plugins.values()
        )



    def load_plugin(self, name):

        try:

            module = importlib.import_module(
                f"plugins.{name}.plugin"
            )

            plugin_class = getattr(
                module,
                "Plugin"
            )

            instance = plugin_class()


            sandbox = PluginSandbox(
                name,
                self.permissions
            )

            self.sandboxes[name] = sandbox


            if hasattr(
                instance,
                "set_sandbox"
            ):

                instance.set_sandbox(
                    sandbox
                )


            self.instances[name] = instance


            return instance


        except Exception:

            self.log(
                traceback.format_exc()
            )

            return None



    def get_sandbox(self, name):

        return self.sandboxes.get(
            name
        )



    def check_permission(
        self,
        name,
        permission
    ):

        return self.permissions.check(
            name,
            permission
        )



    def require_permission(
        self,
        name,
        permission
    ):

        return self.permissions.require(
            name,
            permission
        )



    def start(self, name):

        if name not in self.plugins:
            return False


        plugin = self.load_plugin(
            name
        )


        if not plugin:

            self.plugins[name]["status"] = "ERROR"
            self.save_state()

            return False


        try:

            plugin.start()

            self.plugins[name]["status"] = "RUNNING"

            self.save_state()

            self.log(
                f"{name}: started"
            )

            return True


        except Exception:

            self.plugins[name]["status"] = "ERROR"

            self.save_state()

            self.log(
                traceback.format_exc()
            )

            return False



    def stop(self, name):

        plugin = self.instances.get(
            name
        )

        try:

            if plugin:
                plugin.stop()


            self.plugins[name]["status"] = "STOPPED"

            self.save_state()

            self.log(
                f"{name}: stopped"
            )

            return True


        except Exception:

            self.plugins[name]["status"] = "ERROR"

            self.save_state()

            self.log(
                traceback.format_exc()
            )

            return False



    def auto_start(self):

        for name, data in self.plugins.items():

            if data.get("status") == "RUNNING":

                self.start(name)



plugin_manager = PluginManager()
