import json
import os
import bcrypt

from auth.users.models import User


USERS_FILE = "runtime/users.json"


class UserService:

    def __init__(self):
        self.users = {}
        self.load()


    def hash_password(self, password):
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")


    def check_password(self, password, hashed):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed.encode("utf-8")
        )


    def is_hashed(self, password):
        return password.startswith("$2b$")


    def load(self):

        os.makedirs("runtime", exist_ok=True)

        if not os.path.exists(USERS_FILE):

            self.users = {
                "admin": User(
                    username="admin",
                    password=self.hash_password("admin"),
                    role="admin"
                ),
                "viewer": User(
                    username="viewer",
                    password=self.hash_password("viewer"),
                    role="viewer"
                )
            }

            self.save()
            return


        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)


        migrated = False


        for username, info in data.items():

            password = info["password"]


            # миграция старых открытых паролей
            if not self.is_hashed(password):

                password = self.hash_password(password)
                migrated = True


            self.users[username] = User(
                username=username,
                password=password,
                role=info["role"]
            )


        if migrated:
            self.save()



    def save(self):

        os.makedirs("runtime", exist_ok=True)

        data = {}


        for username, user in self.users.items():

            data[username] = {
                "password": user.password,
                "role": user.role
            }


        with open(
            USERS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )



    def login(
        self,
        username,
        password
    ):

        user = self.users.get(username)


        if not user:
            return None


        if not self.check_password(
            password,
            user.password
        ):
            return None


        return user



    def get(
        self,
        username
    ):

        return self.users.get(username)



    def create(
        self,
        username,
        password,
        role="viewer"
    ):

        user = User(
            username=username,
            password=self.hash_password(password),
            role=role
        )


        self.users[username] = user

        self.save()

        return user



user_service = UserService()
