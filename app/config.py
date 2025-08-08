from pydantic_settings import BaseSettings
from typing import Any
from pathlib import Path
import redis
import logging

class Settings(BaseSettings):
    app_name: str = "IaC server"
    workspace_basedir: str = r"/root/IaC_user_workspace"
    openstack_config: dict[str, Any] = {
        "auth_url": "http://controller:5000/v3/",
        "region": "RegionOne",
        "domain": "Default",
        "endpoints": {
            "compute": "http://controller:8774/v2.1/",
            "identity": "http://controller:5000/v3/",
            "image": "http://controller:9292/v2/",
            # "network": "http://controller:9696/",
            "volumev3": "http://controller:8776/v3/"
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
    redis_conn: dict[str, Any] = {
        "host": "redis",
        "port": 6379
    }
    mongo_conn: dict[str, Any] = {
        "host": "mongodb",
        "port": 27017,
        "db_name": "default_db"  # default database name
    }
    rabbitmq_config: dict[str, Any] = {
        "host": "rabbitmq",
        "credentials": {
            "username": "hoanganh", # dùng env
            "password": "hoanganh"
        },
        "client_ids": {
            "192.168.239.1": 1,
            "portal ip here": 2
        }
    }
    vdi_webhook_url: str = "http://generalserver:8000/webhook"  # replace with

# settings config
settings = Settings()

# redis config
redis_client = redis.Redis(**settings.redis_conn)

# log config
def setup_logger(name, level, filepath):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text('')
    handler = logging.FileHandler(path.as_posix())
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

error_logger = setup_logger("error_logger", logging.ERROR, './log/app.error')
info_logger = setup_logger("info_logger", logging.INFO, './log/app.info')

    