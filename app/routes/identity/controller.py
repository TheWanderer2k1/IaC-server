from .schemas import AuthRequest
from fastapi import Response
import aiohttp
from app.config import settings, redis_client
import json

class AuthController:
    @staticmethod
    async def authentication(auth_request: AuthRequest, response: Response):
        # call openstack authentication server
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{settings.openstack_config.get('endpoints', '').get('identity', '')}auth/tokens", json={"auth": auth_request.model_dump(exclude_none=True)}) as resp:
                try:
                    response_data = await resp.json()
                except aiohttp.ContentTypeError:
                    response_data = await resp.text()
                except json.decoder.JSONDecodeError:
                    response_data = await resp.text()
                if resp.status != 201:
                    response.status_code = resp.status
                    return response_data
                # if authentication is successful, return token
                response.status_code = 201
                token = resp.headers.get("X-Subject-Token", "")
                response.headers["X-Subject-Token"] = token
                # store session in token
                redis_client.set(token, json.dumps(response_data), ex=7200)

                return response_data
