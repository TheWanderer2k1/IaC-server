from pydantic_settings import BaseSettings
from typing import Any
from pathlib import Path
import redis
import logging

class Settings(BaseSettings):
    app_name: str = "IaC server"
    workspace_basedir: str = r"D:\work\projects\IaC_user_workspace"
    openstack_config: dict[str, Any] = {
        "auth_url": "http://controller:5000/v3/",
        "region": "RegionOne",
        "domain": "Default",
        "endpoints": {
            "compute": "http://controller:8774/v2.1/",
            "identity": "http://controller:5000/v3/",
            "image": "http://controller:9292/v2/",
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

# settings config
settings = Settings()

# redis config
redis_conn = {
    "host": "generalserver",
    "port": 6379
}
redis_client = redis.Redis(**redis_conn)

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
# mongo config
mongo_conn = {
    "host": "generalserver",
    "port": 27017,
    "db_name": "default_db"  # default database name
}

# webhook config
vdi_webhook_url = "http://generalserver:8000/webhook"  # replace with
    