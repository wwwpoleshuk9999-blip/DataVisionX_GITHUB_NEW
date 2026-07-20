from core.config import config


class ConfigService:
    """Service for DataVision X configuration."""

    def all(self):
        return config.all()

    def get(self, *keys, default=None):
        return config.get(*keys, default=default)


config_service = ConfigService()
