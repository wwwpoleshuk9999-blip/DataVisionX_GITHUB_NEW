import platform
import sys

from core.config import config


class SystemService:
    """Service for system information."""

    def name(self):
        return config.get(
            "app",
            "name",
            default="DataVision X"
        )

    def version(self):
        return config.get(
            "app",
            "version",
            default="unknown"
        )

    def python_version(self):
        return sys.version

    def platform(self):
        return platform.platform()

    def info(self):
        return {
            "name": self.name(),
            "version": self.version(),
            "python": self.python_version(),
            "platform": self.platform(),
        }


system_service = SystemService()
