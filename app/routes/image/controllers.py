import json
import aiohttp
from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from app.config import settings
from app.base_controller import BaseController
from fastapi import Request
from pathlib import Path
from app.utils.utils import Utils
from app.exceptions.controller_exception import ControllerException

class ImageController(BaseController):
    def __init__(self, 
                 request: Request,
                 cloud_infra_creator: CloudInfrastructureCreator,
                 location: dict[str, str]):
        super().__init__(request, cloud_infra_creator, location)

    async def get_images(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{settings.openstack_config.get('endpoints', {}).get('image', '')}/images", 
                    headers={"X-Auth-Token": self.token}                       
                ) as resp:
                    try:
                        response_data = await resp.json()
                    except aiohttp.ContentTypeError:
                        response_data = await resp.text()
                    except json.decoder.JSONDecodeError:
                        response_data = await resp.text()
                    if resp.status != 200:
                        raise Exception(f"Failed to get images: {response_data}")
                    return response_data
        except Exception as e:
            raise ControllerException(f"An error occurred while getting images: {e}")