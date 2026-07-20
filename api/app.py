from fastapi import FastAPI

from api.routes.health import router as health_router


app = FastAPI(
    title="DataVision X API",
    version="0.3.0"
)


app.include_router(health_router)


@app.get("/")
def root():
    return {
        "name": "DataVision X",
        "status": "ONLINE"
    }
