import secrets
import os


TOKEN_FILE = "runtime/api_token.txt"


class TokenManager:

    def __init__(self):
        self._token = None
        self.load()

    def load(self):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                self._token = f.read().strip()

    def generate(self):
        os.makedirs("runtime", exist_ok=True)

        self._token = secrets.token_hex(32)

        with open(TOKEN_FILE, "w") as f:
            f.write(self._token)

        return self._token

    def get(self):
        if not self._token:
            return self.generate()

        return self._token

    def verify(self, token):
        return token == self._token


token_manager = TokenManager()
