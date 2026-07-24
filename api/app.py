from api.routes.events import router as events_router
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles


from api.routes.health import router as health_router
from api.routes.plugins import router as plugins_router
from api.routes.plugin_lifecycle import router as plugin_lifecycle_router
from api.routes.config import router as config_router
from api.routes.system import router as system_router
from api.routes.dashboard import router as dashboard_router
from api.routes.auth.login import router as auth_router
from api.routes.users import router as users_router
from api.routes.registry import router as registry_router


from auth.middleware import auth_middleware



app = FastAPI(

    title="DataVision X API",

    version="0.3.0"

)



# Web интерфейс

app.mount(

    "/web",

    StaticFiles(
        directory="web",
        html=True
    ),

    name="web"

)



@app.middleware("http")
async def security_middleware(
    request: Request,
    call_next
):


    public_paths = [

        "/auth/login",

        "/web"

    ]


    for path in public_paths:

        if request.url.path.startswith(path):

            return await call_next(
                request
            )


    return await auth_middleware(

        request,

        call_next

    )





# API ROUTES


app.include_router(
    health_router
)


app.include_router(
    plugins_router
)


app.include_router(
    plugin_lifecycle_router
)


app.include_router(
    config_router
)


app.include_router(
    system_router
)


app.include_router(
    dashboard_router
)


app.include_router(
    auth_router
)


app.include_router(
    users_router
)


app.include_router(
    registry_router
)

app.include_router(
    events_router
)
