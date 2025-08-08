from huey import RedisHuey
from app.config import settings
from app.exceptions.queuejob_exception import QueueJobException
import aiohttp
import json
from app.config import info_logger, error_logger
from app.exceptions.datastore_exception import DatastoreOperationException
from app.database.factories.mongo_datastore_creator import mongo_creator
from datetime import datetime
from app.core.msg_queue.rabbitmq_queue import RabbitMQQueue

# queue init
huey = RedisHuey('huey-queue', **settings.redis_conn, db=0)

# format the data
def prepare_body(data):
    if isinstance(data, (dict, list)):
        return json.dumps(data)
    return str(data)  # stringifies everything else

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
def run_job(host_ip: str, func, **kwargs):
    try:
        result = func(**kwargs)
        info_logger.info(f"Job completed with result: {result}")
        msg_queue = RabbitMQQueue(host_ip)
        msg_queue.publish_result(host_ip, prepare_body(result))
    except Exception as e:
        msg_queue.emit_error(host_ip, prepare_body(e))
        raise QueueJobException(f"Exception in job: {e}")
    finally:
        msg_queue.close_connection()
    
# custom task only for run infra job
@huey.task()
def run_infra_job(host_ip: str, obj, method_name, **kwargs):
    try:
        func = getattr(obj, method_name)
        result = func(**kwargs)
        info_logger.info(f"Job completed with result: {result}")
        # send message to vdi
        msg_queue = RabbitMQQueue(host_ip)
        msg_queue.publish_result(host_ip, prepare_body(result))
        # backup to mongodb
        try:
            mongo_datastore = mongo_creator.create_datastore()
            document = obj.cloud_infra.backup_infra()
            # get the current backup document
            backup_data = mongo_datastore.find("infra_backup", {"path_to_tf_workspace": obj.cloud_infra.path_to_tf_workspace})
            if backup_data and backup_data[0]['backup_data']:
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
        # emit message to vdi
        msg_queue.emit_error(host_ip, prepare_body(e3))
        raise QueueJobException(f"Exception in infra job: {e3}")
    finally:
        msg_queue.close_connection()
