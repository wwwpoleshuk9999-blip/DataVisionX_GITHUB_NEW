from pathlib import Path
import yaml

CONFIG_FILE = Path("config.yaml")

class Config:
    def __init__(self):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    def get(self, *keys, default=None):
        value = self.data
        for key in keys:
            if not isinstance(value, dict):
                return default
            value = value.get(key)
            if value is None:
                return default
        return value

config = Config()
