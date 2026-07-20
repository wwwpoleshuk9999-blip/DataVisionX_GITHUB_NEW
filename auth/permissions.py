class PermissionManager:
    """Manage DataVision X permissions."""

    def __init__(self):
        self.permissions = {
            "admin": [
                "read",
                "write",
                "manage"
            ],
            "viewer": [
                "read"
            ]
        }

    def get(self, role):
        return self.permissions.get(
            role,
            []
        )

    def check(self, role, permission):
        return permission in self.get(role)


permission_manager = PermissionManager()
