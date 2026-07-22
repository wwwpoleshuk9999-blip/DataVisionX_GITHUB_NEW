import os
import json
import importlib
import traceback


PLUGINS_DIR = "plugins"
RUNTIME_FILE = "runtime/plugins.json"
LOG_FILE = "runtime/plugins.log"


class PluginManager:

    def __init__(self):

        self.plugins = {}
        self.instances = {}

        self.load_state()
        self.scan_plugins()
        self.auto_start()



    def log(self, message):

        os.makedirs("runtime", exist_ok=True)

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(message + "\n")



    def load_state(self):

        os.makedirs(
            "runtime",
            exist_ok=True
        )

        if os.path.exists(RUNTIME_FILE):

            with open(
                RUNTIME_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                self.plugins = json.load(f)



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


        for name in os.listdir(PLUGINS_DIR):

            path = os.path.join(
                PLUGINS_DIR,
                name
            )


            if not os.path.isdir(path):
                continue


            manifest = os.path.join(
                path,
                "manifest.json"
            )


            if not os.path.exists(manifest):
                continue


            with open(
                manifest,
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

                    "status": "STOPPED"
                }


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


            self.instances[name] = instance


            return instance


        except Exception:

            self.log(
                traceback.format_exc()
            )

            return None



    def start(self, name):

        if name not in self.plugins:

            return False


        plugin = self.load_plugin(name)


        if not plugin:

            self.plugins[name]["status"] = "ERROR"
            self.save_state()

            return False



        try:

            plugin.start()


            self.plugins[name]["status"] = "LOADED"

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

        plugin = self.instances.get(name)


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

            if data.get("status") == "LOADED":

                self.start(name)



plugin_manager = PluginManager()
