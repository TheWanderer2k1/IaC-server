from huey import RedisHuey
from app.config import redis_conn, vdi_webhook_url
from app.exceptions.queuejob_exception import QueueJobException
import aiohttp
import asyncio
from app.config import vdi_webhook_url
import json
from app.config import info_logger, error_logger
from app.exceptions.datastore_exception import DatastoreOperationException
from app.database.factories.mongo_datastore_creator import mongo_creator
from datetime import datetime
from app.core.msg_queue.rabbitmq_queue import RabbitMQQueue

# queue init
huey = RedisHuey('huey-queue', **redis_conn, db=0)

msg_queue = RabbitMQQueue().get_instance()
msg_queue.create_channel("vdi")

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
        msg_queue.publish_result("vdi", result)
    except Exception as e:
        msg_queue.emit_error("vdi", e)
        raise QueueJobException(f"Exception in job: {e}")
    
# custom task only for run infra job
@huey.task()
def run_infra_job(obj, method_name, **kwargs):
    try:
        func = getattr(obj, method_name)
        result = func(**kwargs)
        info_logger.info(f"Job completed with result: {result}")
        try:
            asyncio.run(make_http_request(vdi_webhook_url, {"result": result}))
            info_logger.info(f"Webhook called successfully with result: {result}")
        except Exception as e1:
            error_logger.error(f"Failed to call webhook: {e1}")
            pass
        # backup to mongodb
        try:
            mongo_datastore = mongo_creator.create_datastore()
            document = obj.cloud_infra.backup_infra()
            # get the current backup document
            backup_data = mongo_datastore.find("infra_backup", {"path_to_tf_workspace": obj.cloud_infra.path_to_tf_workspace})
            if backup_data[0]['backup_data']:
                document = document + backup_data[0]['backup_data']
            mongo_datastore.update("infra_backup", 
                {"path_to_tf_workspace": obj.cloud_infra.path_to_tf_workspace}, 
                {
                    "backup_data": document,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            )
        except Exception as e2:
            error_logger.error(f"Failed to backup: {e2}")
            pass
    except Exception as e3:
        # gọi webhook báo exception
        try:
            asyncio.run(make_http_request(vdi_webhook_url, {"error": e3}))
            info_logger.error(f"Exception in job: {e3}")
        except Exception as e4:
            error_logger.error(f"Failed to call webhook: {e4}")
            pass
        raise QueueJobException(f"Exception in infra job: {e3}")
