import datetime


class PermissionManager:

    def __init__(self, plugin_manager):

        self.plugin_manager = plugin_manager


    def check(self, plugin_id, permission):

        plugin = self.plugin_manager.plugins.get(
            plugin_id
        )

        if not plugin:
            return False


        permissions = plugin.get(
            "permissions",
            {}
        )

        return permissions.get(
            permission,
            False
        )


    def require(self, plugin_id, permission):

        allowed = self.check(
            plugin_id,
            permission
        )

        if allowed:
            return True


        self.audit(
            plugin_id,
            permission
        )

        return False


    def audit(self, plugin_id, permission):

        with open(
            "runtime/security.log",
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"{datetime.datetime.now()} | "
                f"{plugin_id} | "
                f"{permission} | BLOCKED\n"
            )
