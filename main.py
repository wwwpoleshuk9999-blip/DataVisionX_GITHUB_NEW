from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from core.kernel import Kernel
from core.health import health
from api.ai import router as ai_router
from api.routes.metrics import router as metrics_router

from api.routes.health import router as health_router
from api.routes.plugins import router as plugins_router
from api.routes.system import router as system_router
from api.routes.dashboard import router as dashboard_router
from api.routes.users import router as users_router
from api.routes.watchdog import router as watchdog_router
from api.routes.plugin_lifecycle import router as plugin_lifecycle_router
from api.routes.events import router as events_router
from api.routes.registry import router as registry_router
from api.routes.runtime import router as runtime_router
from api.routes.recovery import router as recovery_router
from api.routes.plugin_health import router as plugin_health_router
from api.routes.websocket import router as websocket_router
from api.routes.devtools import router as devtools_router



app = FastAPI(
    title="DataVisionX API",
    version="0.5.0"
)


app.include_router(ai_router)
app.include_router(metrics_router)

app.include_router(health_router)
app.include_router(plugins_router)
app.include_router(system_router)
app.include_router(dashboard_router)
app.include_router(users_router)
app.include_router(watchdog_router)
app.include_router(plugin_lifecycle_router)
app.include_router(events_router)
app.include_router(registry_router)
app.include_router(runtime_router)
app.include_router(recovery_router)
app.include_router(plugin_health_router)
app.include_router(websocket_router)
app.include_router(devtools_router)


app.mount('/web', StaticFiles(directory='web'), name='web')


kernel = Kernel()


@app.on_event("startup")
def startup():
    kernel.start()


@app.on_event("shutdown")
def shutdown():
    kernel.stop()


@app.get("/")
def dashboard():
    return FileResponse("web/index.html")


@app.get("/api/status")
def api_status():
    return {
        "name": "DataVisionX",
        "status": "ONLINE"
    }


@app.get("/health")
def health_check():
    return health.report()
