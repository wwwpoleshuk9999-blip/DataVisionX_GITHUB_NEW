from fastapi import FastAPI, Request

from api.routes.health import router as health_router
from api.routes.plugins import router as plugins_router
from api.routes.config import router as config_router
from api.routes.system import router as system_router

from auth.middleware import auth_middleware


app = FastAPI(
    title="DataVision X API",
    version="0.3.0"
)


@app.middleware("http")
async def security_middleware(
    request: Request,
    call_next
):
    return await auth_middleware(
        request,
        call_next
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
