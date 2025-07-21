from pydantic_settings import BaseSettings
from typing import Any
from huey import RedisHuey

class Settings(BaseSettings):
    app_name: str = "IaC server"
    workspace_basedir: str = r"D:\work_folder\Projects\IaC_user_workspace"
    openstack_config: dict[str, Any] = {
        "identity_endpoint": "http://controller:5000",
        "provider_mapping": {
            "Epoxy": "",
            "Dalmatian": "",
            "Caracal": "3.0.0",
            "Bobcat": "",
            "Antelope": "",
            "Zed": "",
            "Yoga": "3.0.0",
            "Train": ""
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

huey = RedisHuey('huey-queue', **redis_conn, db=0)
# nếu dùng huey, phải register task tại compile time nếu ko consumer sẽ không tìm thấy task trong registry
@huey.task()
def run_job(func, **kwargs):
    return func(**kwargs)
    