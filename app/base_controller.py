from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from fastapi import Request
from .config import settings
from pathlib import Path
import json

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

    def create_resource(self, resource_type: str, resource_name: str, resource_value: dict[str, str]):
        try:
            self.cloud_infra.add_resource(
                tf_resource_type=resource_type,
                tf_resource_name=resource_name,
                tf_resource_values=resource_value)
            # apply infra object
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
            raise Exception(e)
        
    def modify_resource(self, resource_type: str, resource_id: str, resource_value: dict[str, str]):
        try:
            # tf_resource_type, tf_resource_name lấy từ tfstate file
            with open(f"{self.user_workspace_path}/terraform.tfstate", "r") as f:
                tfstate = json.load(f)
            for resource in tfstate.get('resources', []):
                for instance in resource.get('instances', []):
                    if instance.get('attributes', {}).get('id', "") == resource_id and \
                        resource.get("type") == resource_type :
                        resource_name = resource.get("name")
                        break
            # modify resource
            self.cloud_infra.modify_resource(
                resource_type=resource_type,
                resource_name=resource_name,
                resource_value=resource_value
            )
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
            raise Exception(e)

    def delete_resource(self, resource_type: str, resource_id: str):
        try:
            # tf_resource_type, tf_resource_name lấy từ tfstate file
            with open(f"{self.user_workspace_path}/terraform.tfstate", "r") as f:
                tfstate = json.load(f)
            for resource in tfstate.get('resources', []):
                for instance in resource.get('instances', []):
                    if instance.get('attributes', {}).get('id', "") == resource_id and \
                        resource.get("type") == resource_type :
                        resource_name = resource.get("name")
                        break
            # delete resource
            self.cloud_infra.delete_resource(
                tf_resource_type=resource_type,
                tf_resource_name=resource_name
            )
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
            raise Exception(e)