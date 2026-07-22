from fastapi import FastAPI, Request

from api.routes.health import router as health_router
from api.routes.plugins import router as plugins_router
from api.routes.config import router as config_router
from api.routes.system import router as system_router
from api.routes.auth.login import router as auth_router
from api.routes.users import router as users_router

from auth.middleware import auth_middleware

app = FastAPI(
    title="DataVision X API",
    version="0.3.0"
)


@app.middleware("http")
async def security_middleware(request: Request, call_next):

    if request.url.path.startswith("/auth/login"):
        return await call_next(request)

    return await auth_middleware(
        request,
        call_next
    )


app.include_router(health_router)
app.include_router(plugins_router)
app.include_router(config_router)
app.include_router(system_router)
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {
        "name": "DataVision X",
        "status": "ONLINE"
    }
