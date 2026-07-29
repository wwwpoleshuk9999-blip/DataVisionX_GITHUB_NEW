from fastapi import FastAPI

from core.kernel import Kernel
from core.health import health
from api.ai import router as ai_router


app = FastAPI(
    title="DataVisionX API",
    version="0.5.0"
)


app.include_router(ai_router)


kernel = Kernel()


@app.on_event("startup")
def startup():
    kernel.start()


@app.on_event("shutdown")
def shutdown():
    kernel.stop()


@app.get("/")
def root():
    return {
        "name": "DataVisionX",
        "status": "ONLINE"
    }


@app.get("/health")
def health_check():
    return health.report()
