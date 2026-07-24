from fastapi import APIRouter
import platform
import sys
import time

router = APIRouter()

START_TIME = time.time()


@router.get("/system")
def system():

    uptime = int(time.time() - START_TIME)

    return {
        "status": "RUNNING",
        "health": "HEALTHY",
        "version": "0.5 Phoenix",
        "python": sys.version.split()[0],
        "platform": platform.system(),
        "uptime": uptime
    }
