from core.runtime import runtime


class RuntimeService:
    """Service for managing the DataVision X runtime."""

    def start(self):
        runtime.start()

    def stop(self):
        runtime.stop()

    def status(self):
        return runtime.status()

    def uptime(self):
        return runtime.uptime()


runtime_service = RuntimeService()
