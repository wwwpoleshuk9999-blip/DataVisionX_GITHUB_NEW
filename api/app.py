from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.plugins import router as plugins_router
from api.routes.config import router as config_router
from api.routes.system import router as system_router


app = FastAPI(
    title="DataVision X API",
    version="0.3.0"
)


app.include_router(health_router)
app.include_router(plugins_router)
app.include_router(config_router)
app.include_router(system_router)


@app.get("/")
def root():
    return {
        "name": "DataVision X",
        "status": "ONLINE"
    }
