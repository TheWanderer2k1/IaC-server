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
        endpoint_overrides = settings.openstack_config.get("endpoints", {})
        self.cloud_infra = self.cloud_infra_creator.create_infrastructure(
            path_to_tf_workspace=self.user_workspace_path,
            provider_version=settings.openstack_config.get("provider_mapping", "").get("Yoga", ""),
            auth_url=settings.openstack_config.get('auth_url', ''),
            region=location.get('region'),
            token=request.headers.get("X-Subject-Token"),
            tenant_name=location.get('project'),
            endpoint_overrides=endpoint_overrides
        )

    def create_resource(self, resource_type: str, resource_name: str, resource_values: dict[str, str]):
        try:
            self.cloud_infra.add_resource(
                resource_type=resource_type,
                resource_name=resource_name,
                resource_values=resource_values)
            # apply infra object
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
            raise Exception(e)
        
    def modify_resource(self, resource_type: str, resource_id: str, resource_values: dict[str, str]):
        try:
            # resource_type, resource_name lấy từ tfstate file
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
                resource_values=resource_values
            )
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
            raise Exception(e)

    def delete_resource(self, resource_type: str, resource_id: str):
        try:
            # resource_type, resource_name lấy từ tfstate file
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
                resource_type=resource_type,
                resource_name=resource_name
            )
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
            raise Exception(e)
        
    def import_resource(self, resource_type: str, resource_name: str, resource_id: str):
        try:
            self.cloud_infra.import_resource(resource_type, resource_name, resource_id)
            return True
        except Exception as e:
            raise Exception(e)