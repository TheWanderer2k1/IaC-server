from .schemas import AuthRequest
from fastapi import Response
import aiohttp
from app.config import settings

class AuthController:
    @staticmethod
    async def authentication(auth_request: AuthRequest, response: Response):
        # call openstack authentication server
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{settings.openstack_config.get('endpoints', '').get('identity', '')}auth/tokens", json={"auth": auth_request.model_dump(exclude_none=True)}) as resp:
                response_data = await resp.json()
                if resp.status != 201:
                    response.status_code = resp.status
                    return response_data
                # if authentication is successful, return token
                response.status_code = 201
                response.headers["X-Subject-Token"] = resp.headers.get("X-Subject-Token", "")
                return response_data
