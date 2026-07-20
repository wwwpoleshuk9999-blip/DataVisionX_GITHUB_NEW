from fastapi import Request
from fastapi.responses import JSONResponse

from auth.token import token_manager


async def auth_middleware(request: Request, call_next):

    public_paths = [
        "/",
        "/health",
        "/docs",
        "/openapi.json"
    ]

    if request.url.path in public_paths:
        return await call_next(request)

    token = request.headers.get("X-API-Key")

    if not token or not token_manager.verify(token):
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid API Key"
            }
        )

    return await call_next(request)
