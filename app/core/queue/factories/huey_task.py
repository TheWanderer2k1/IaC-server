from huey import RedisHuey
from app.config import redis_conn, vdi_webhook_url
from app.exceptions.queuejob_exception import QueueJobException
import aiohttp
import asyncio
from app.config import vdi_webhook_url
import json
from app.config import info_logger, error_logger

# queue init
huey = RedisHuey('huey-queue', **redis_conn, db=0)

# make http request
async def make_http_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            if resp.status != 200:
                raise Exception(f"HTTP request failed with status {resp.status}")
            try:
                response_data = await resp.json()
            except aiohttp.ContentTypeError:
                response_data = await resp.text()
            except json.decoder.JSONDecodeError:
                response_data = await resp.text()
            return response_data

# register task
@huey.task()
def run_job(func, **kwargs):
    try:
        result = func(**kwargs)
        info_logger.info(f"Job completed with result: {result}")
        try:
            asyncio.run(make_http_request(vdi_webhook_url, {"result": result}))
            info_logger.info(f"Webhook called successfully with result: {result}")
        except Exception as e:
            error_logger.error(f"Failed to call webhook: {e}")
            pass
    except Exception as e:
        # gọi webhook báo exception
        try:
            asyncio.run(make_http_request(vdi_webhook_url, {"error": e}))
            info_logger.error(f"Exception in job: {e}")
        except Exception as e:
            error_logger.error(f"Failed to call webhook: {e}")
            pass
        raise QueueJobException(f"Exception in job: {e}")
