import json
import secrets
from pathlib import Path


RUNTIME_DIR = Path("runtime")
RUNTIME_DIR.mkdir(exist_ok=True)

SESSIONS_FILE = RUNTIME_DIR / "sessions.json"


class SessionManager:

    def __init__(self):
        self.sessions = {}
        self.load()

    def load(self):
        if SESSIONS_FILE.exists():
            try:
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                    self.sessions = json.load(f)
            except Exception:
                self.sessions = {}

    def save(self):
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.sessions, f, indent=4)

    def create(self, username):
        token = secrets.token_hex(32)
        self.sessions[token] = username
        self.save()
        return token

    def get_user(self, token):
        return self.sessions.get(token)

    def delete(self, token):
        if token in self.sessions:
            del self.sessions[token]
            self.save()

    def all(self):
        return self.sessions


session_manager = SessionManager()
