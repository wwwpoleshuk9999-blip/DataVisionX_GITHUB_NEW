import os
import json


STORAGE_DIR = "runtime/plugin_storage"


class PluginStorage:

    def __init__(self, permission_manager):

        self.permissions = permission_manager

        os.makedirs(
            STORAGE_DIR,
            exist_ok=True
        )


    def _file(self, plugin_id):

        path = os.path.join(
            STORAGE_DIR,
            plugin_id
        )

        os.makedirs(
            path,
            exist_ok=True
        )

        return os.path.join(
            path,
            "data.json"
        )


    def _load(self, plugin_id):

        file = self._file(
            plugin_id
        )

        if not os.path.exists(file):

            return {}


        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def _save(self, plugin_id, data):

        with open(
            self._file(plugin_id),
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )



    def set(self, plugin_id, key, value):

        if not self.permissions.require(
            plugin_id,
            "storage"
        ):

            return False


        data = self._load(
            plugin_id
        )

        data[key] = value

        self._save(
            plugin_id,
            data
        )

        return True



    def get(self, plugin_id, key):

        if not self.permissions.require(
            plugin_id,
            "storage"
        ):

            return None


        data = self._load(
            plugin_id
        )

        return data.get(
            key
        )



    def delete(self, plugin_id, key):

        if not self.permissions.require(
            plugin_id,
            "storage"
        ):

            return False


        data = self._load(
            plugin_id
        )

        if key in data:

            del data[key]

            self._save(
                plugin_id,
                data
            )

        return True
