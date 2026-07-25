from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from api.routes.events import router as events_router
from api.routes.health import router as health_router
from api.routes.plugins import router as plugins_router
from api.routes.plugin_lifecycle import router as plugin_lifecycle_router
from api.routes.config import router as config_router
from api.routes.system import router as system_router
from api.routes.dashboard import router as dashboard_router
from api.routes.auth.login import router as auth_router
from api.routes.users import router as users_router
from api.routes.registry import router as registry_router
from api.routes.runtime import router as runtime_router
from api.routes.watchdog import router as watchdog_router
from api.routes.recovery import router as recovery_router
from api.routes.recovery_test import router as recovery_test_router

from auth.middleware import auth_middleware

from core.service import service
from core.runtime import runtime


@asynccontextmanager
async def lifespan(app: FastAPI):
    service.save_pid()
    runtime.start()

    try:
        yield
    finally:
        runtime.stop()
        service.remove_pid()


app = FastAPI(
    title="DataVision X API",
    version="0.3.1",
    lifespan=lifespan,
)

app.mount(
    "/web",
    StaticFiles(
        directory="web",
        html=True,
    ),
    name="web",
)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    public_paths = [
        "/auth/login",
        "/web",
    ]

    for path in public_paths:
        if request.url.path.startswith(path):
            return await call_next(request)

    return await auth_middleware(request, call_next)


app.include_router(health_router)
app.include_router(plugins_router)
app.include_router(plugin_lifecycle_router)
app.include_router(config_router)
app.include_router(system_router)
app.include_router(dashboard_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(registry_router)
app.include_router(events_router)
app.include_router(runtime_router)
app.include_router(watchdog_router)
app.include_router(recovery_router)
app.include_router(recovery_test_router)
