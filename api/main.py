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
from api.routes.plugin_health import router as plugin_health_router
from api.routes.auth.login import router as auth_router
from api.routes.users import router as users_router
from api.routes.websocket import router as websocket_router
from api.routes.ai import router as ai_router
from api.routes.ai_agents import router as ai_agents_router

from auth.middleware import auth_middleware

import services.register_eventbus
from core.bootstrap import register_core_services
from services.websocket_bridge import set_loop
import asyncio
from contextlib import asynccontextmanager
from core.runtime import runtime
from core.service import service
from core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    service.save_pid()
    runtime.start()
    set_loop(asyncio.get_running_loop())

    from plugin_manager.manager import plugin_manager

    plugin_manager.discover()

    for plugin in plugin_manager.list_plugins():
        try:
            plugin_manager.start(plugin.id)
        except Exception as e:
            logger.error(f"Failed to start plugin {plugin.id}: {e}")

    try:
        yield
    finally:
        runtime.stop()
        service.remove_pid()

app = FastAPI(
    title="DataVisionX API",
    version="0.5 Phoenix Beta",
    lifespan=lifespan,
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
app.include_router(plugin_health_router)
app.include_router(ai_router)
app.include_router(ai_agents_router)

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

from services.websocket_manager import manager
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

@app.websocket("/ws")
async def websocket_direct(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await manager.send(websocket, "Connected to DataVisionX Phoenix")
        while True:
            await asyncio.sleep(30)
            await manager.send(websocket, "ping")
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)

# Phoenix 015 Dashboard 2.0
try:
    from web.dashboard_v2 import router as dashboard_v2_router
    app.include_router(dashboard_v2_router)
except Exception as e:
    print(f"Dashboard v2 not loaded: {e}")

# Phoenix 020 Dashboard 3.0 React 100% MAX
try:
    from web.dashboard_v3 import router as dashboard_v3_router
    try:
        from web.dashboard_v5 import router as dashboard_v5_router
        app.include_router(dashboard_v5_router)
    except Exception as e:
        print(f"Dashboard v5 not loaded: {e}")
    try:
        from api.routes.ultimate import router as ultimate_router
        app.include_router(ultimate_router)
    except Exception as e:
        print(f"Ultimate API not loaded: {e}")
    app.include_router(dashboard_v3_router)
except Exception as e:
    print(f"Dashboard v3 not loaded: {e}")

# Phoenix 050 Ultimate AGI
try:
    from web.dashboard_v5 import router as dashboard_v5_router
    app.include_router(dashboard_v5_router)
except Exception as e:
    print(f"Dashboard v5 not loaded: {e}")

try:
    from api.routes.ultimate import router as ultimate_router
    app.include_router(ultimate_router)
except Exception as e:
    print(f"Ultimate API not loaded: {e}")

# Phoenix 100 SUPER AGI Dashboard 6.0
try:
    from web.dashboard_v6 import router as dashboard_v6_router
    app.include_router(dashboard_v6_router)
except Exception as e:
    print(f"Dashboard v6 not loaded: {e}")

# Phoenix 200 BUSINESS AGI Dashboard 7.0 + Business API
try:
    from web.dashboard_v7 import router as dashboard_v7_router
    app.include_router(dashboard_v7_router)
except Exception as e:
    print(f"Dashboard v7 not loaded: {e}")

try:
    from api.routes.business import router as business_router
    app.include_router(business_router)
except Exception as e:
    print(f"Business API not loaded: {e}")

# Phoenix 1000 GOD AGI Dashboard 10.0 + GOD API
try:
    from web.dashboard_v10 import router as dashboard_v10_router
    app.include_router(dashboard_v10_router)
except Exception as e:
    print(f"Dashboard v10 not loaded: {e}")

try:
    from api.routes.god import router as god_router
    app.include_router(god_router)
except Exception as e:
    print(f"GOD API not loaded: {e}")
