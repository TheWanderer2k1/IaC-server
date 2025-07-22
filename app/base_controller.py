from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from fastapi import Request
from .config import settings
from pathlib import Path

class BaseController:
    def __init__(self,
                 request: Request,
                 cloud_infra_creator: CloudInfrastructureCreator,
                 location: dict[str, str]):
        self.cloud_infra_creator = cloud_infra_creator
        self.location = location
        self.user_workspace_path = settings.workspace_basedir + f"/{location.get('domain')}/{location.get('project')}/{location.get('username')}"
        # init the user environment if not exists
        dir_path = Path(self.user_workspace_path)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            # git init here
            # tf init here
            # 
        self.cloud_infra = self.cloud_infra_creator.create_infrastructure(
            path_to_tf_workspace=self.user_workspace_path,
            provider_version=settings.openstack_config.get("provider_mapping", "").get("Yoga", ""),
            auth_url=f"{settings.openstack_config.get('endpoints', '').get('identity', '')}",
            region=f"{location.get('region')}",
            token=request.headers.get("X-Subject-Token"),
            tenant_name=f"{location.get('project')}"
        )