from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch = None):
        super().__init__(app, dispatch)
        self.exclude_routes = ["/v3/auth/tokens",
                               "/docs",
                               "/openapi.json"]

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in self.exclude_routes and not request.headers.get("X-Subject-Token"):
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized!"}
            )
        # add username, project, domain to memory cache ?

        response = await call_next(request)
        return response