from auth.users.models import User


class UserService:

    def __init__(self):
        self.users = {
            "admin": User(
                username="admin",
                password="admin",
                role="admin"
            ),
            "viewer": User(
                username="viewer",
                password="viewer",
                role="viewer"
            )
        }

    def login(self, username, password):
        user = self.users.get(username)

        if not user:
            return None

        if user.password != password:
            return None

        return user

    def get(self, username):
        return self.users.get(username)


user_service = UserService()
