from fastapi import FastAPI

from api.routes.plugins import router as plugins_router


app = FastAPI(
    title="DataVisionX API",
    version="0.5"
)


app.include_router(
    plugins_router
)


@app.get("/")
def home():

    return {
        "name": "DataVisionX",
        "version": "0.5",
        "status": "RUNNING"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
