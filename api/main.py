from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.routes.health import router as health_router
from api.routes.plugins import router as plugins_router
from api.routes.plugin_lifecycle import router as plugin_lifecycle_router
from api.routes.config import router as config_router
from api.routes.system import router as system_router
from api.routes.dashboard import router as dashboard_router
from api.routes.registry import router as registry_router
from api.routes.events import router as events_router
from api.routes.auth.login import router as auth_router
from api.routes.users import router as users_router
from api.routes.websocket import router as websocket_router
from api.routes.ai import router as ai_router

from auth.middleware import auth_middleware
from core.bootstrap import register_core_services
from services.websocket_bridge import set_loop
import asyncio


app = FastAPI(
    title="DataVisionX API",
    version="0.5 Phoenix Beta"
)


@app.middleware("http")
async def security_middleware(request: Request, call_next):

    if (
        request.url.path.startswith("/auth/login")
        or request.url.path.startswith("/ws")
    ):
        return await call_next(request)

    try:
        return await auth_middleware(request, call_next)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )


# -----------------------
# API ROUTES
# -----------------------

app.include_router(health_router)
app.include_router(system_router)
app.include_router(plugins_router)
app.include_router(plugin_lifecycle_router)
app.include_router(config_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(dashboard_router)
app.include_router(websocket_router)
app.include_router(registry_router)
app.include_router(events_router)
app.include_router(ai_router)


# -----------------------
# WEB
# -----------------------

app.mount(
    "/web",
    StaticFiles(directory="web"),
    name="web"
)


@app.get("/")
def root():

    return {
        "name": "DataVisionX",
        "version": "0.5 Phoenix Beta",
        "status": "RUNNING"
    }


@app.get("/dashboard")
def dashboard():

    return FileResponse(
        "web/index.html"
    )


@app.get("/web/")
def web_home():

    return FileResponse(
        "web/index.html"
    )


@app.on_event("startup")
async def websocket_loop_init():
    set_loop(asyncio.get_running_loop())
