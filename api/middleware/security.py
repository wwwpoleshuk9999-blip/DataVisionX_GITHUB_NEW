from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit=100):
        super().__init__(app)
        self.rate_limit=rate_limit
        self.requests=defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        ip=request.client.host if request.client else "unknown"
        now=time.time()
        self.requests[ip]=[t for t in self.requests[ip] if now-t<60]
        if len(self.requests[ip])>=self.rate_limit:
            from fastapi.responses import JSONResponse
            return JSONResponse({"error": "Rate limit"}, status_code=429)
        self.requests[ip].append(now)
        response=await call_next(request)
        response.headers["X-Content-Type-Options"]="nosniff"
        response.headers["X-Frame-Options"]="DENY"
        response.headers["X-XSS-Protection"]="1; mode=block"
        return response
