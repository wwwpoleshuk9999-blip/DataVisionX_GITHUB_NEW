from fastapi import APIRouter

from core.metrics import metrics

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

_history = []


@router.get("/system")
def system_metrics():
    data = metrics.system()

    _history.append(data)
    if len(_history) > 100:
        _history.pop(0)

    return data


@router.get("/runtime")
def runtime_metrics():
    return {
        "status": "RUNNING",
        "metrics_collected": len(_history)
    }


@router.get("/history")
def history_metrics(limit: int = 100):

    return {
        "count": len(_history),
        "history": _history[-limit:]
    }
