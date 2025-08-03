import json
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.config import redis_client, settings
from urllib.parse import urlencode

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch = None):
        super().__init__(app, dispatch)
        self.exclude_routes = ["/v3/auth/tokens",
                               "/docs",
                               "/openapi.json",
                               "/infra/test"]

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("X-Subject-Token")
        if request.url.path not in self.exclude_routes and not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized!"}
            )
        elif request.url.path not in self.exclude_routes and token:
            try:
                # get region, domain, project, username from memory cache
                user_session = redis_client.get(token)
                if not user_session:
                    return JSONResponse(
                        status_code=404,
                        content={"detail": "Session not found!"}
                    )
                session_data = json.loads(user_session)
                query_params = dict(request.query_params)
                query_params["region"] = settings.openstack_config.get("region")
                query_params["domain"] = settings.openstack_config.get("domain")
                query_params["project"] = session_data["token"]["project"]["name"]
                query_params["username"] = session_data["token"]["user"]["name"]
                request.scope["query_string"] = urlencode(query_params).encode("utf-8")
            except Exception as e:
                return JSONResponse(
                status_code=500,
                content={"detail": e}
            )
        response = await call_next(request)
        return response