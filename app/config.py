from pydantic_settings import BaseSettings
from typing import Any
from huey import RedisHuey
import redis

class Settings(BaseSettings):
    app_name: str = "IaC server"
    workspace_basedir: str = r"D:\work_folder\Projects\IaC_user_workspace"
    openstack_config: dict[str, Any] = {
        "region": "RegionOne",
        "domain": "Default",
        "endpoints": {
            # "compute": "http://controller:8774/v2.1/",
            "identity": "http://controller:5000/v3/",
            # "image": "http://controller:9292/",
            # "network": "http://controller:9696/",
            # "volumev3": ""
        },
        "provider_mapping": {
            "Epoxy": "3.0.0",
            "Dalmatian": "3.0.0",
            "Caracal": "3.0.0",
            "Bobcat": "3.0.0",
            "Antelope": "3.0.0",
            "Zed": "3.0.0",
            "Yoga": "3.0.0",
            "Train": "3.0.0"
        },
        "db_config": {
            "host": "",
            "database": "",
            "username": "",
            "password": ""
        }
    }

settings = Settings()
redis_conn = {
    "host": "192.168.239.155",
    "port": 6379
}

redis_client = redis.Redis(**redis_conn)
huey = RedisHuey('huey-queue', **redis_conn, db=0)
# nếu dùng huey, phải register task tại compile time nếu ko consumer sẽ không tìm thấy task trong registry
@huey.task()
def run_job(func, **kwargs):
    return func(**kwargs)
    