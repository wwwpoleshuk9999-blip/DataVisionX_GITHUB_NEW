from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str
    role: str

    def to_dict(self):
        return {
            "username": self.username,
            "role": self.role
        }
