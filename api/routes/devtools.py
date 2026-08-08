from fastapi import APIRouter

from devtools.manager.manager import DevToolsManager

router = APIRouter(prefix="/api/devtools", tags=["devtools"])


@router.get("")
def devtools_report():
    manager = DevToolsManager()
    return manager.run("devtools")


@router.get("/run")
def devtools_run():
    manager = DevToolsManager()
    return manager.run("devtools")


@router.get("/health")
def devtools_health():
    manager = DevToolsManager()
    report = manager.run("devtools")

    return {
        "status": report.get("status", "UNKNOWN"),
        "diagnosis": report.get("diagnosis", {}),
        "safety": report.get("safety", {}),
    }
