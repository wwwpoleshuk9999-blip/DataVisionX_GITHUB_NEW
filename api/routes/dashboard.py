from fastapi import APIRouter
from core.health import get_health_report

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("")
def dashboard():
    health = get_health_report()

    return {
        "project": "DataVisionX",
        "version": "0.3.0",
        "status": health.get("status", "UNKNOWN"),
        "uptime": health.get("uptime", 0),
        "health": health.get("health", "UNKNOWN")
    }
