from core.health import health


class HealthService:
    """Service for system health monitoring."""

    def report(self):
        return health.report()

    def status(self):
        data = health.report()
        return data.get("status")

    def is_healthy(self):
        data = health.report()
        return data.get("status") == "HEALTHY"


health_service = HealthService()
