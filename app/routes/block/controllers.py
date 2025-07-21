import json
from .schemas import BlockVolumeCreateRequest
from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from fastapi import Request
from app.config import settings
from pathlib import Path

class BlockVolumeController: 
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

    def create_volume(self, block_volume_create_request: BlockVolumeCreateRequest):
        try:
            # generate infra object
            block_volume_config = block_volume_create_request.model_dump(exclude_none=True)
            self.cloud_infra.add_resource(
                tf_resource_type="openstack_blockstorage_volume_v3",
                tf_resource_name=f"openstack_blockstorage_volume_v3_{self.location.get('domain')}_{self.location.get('project')}_{self.location.get('username')}_dwadad", # auto generated name
                tf_resource_values={
                    "size": block_volume_config["volume"].get("size", None),
                    "source_vol_id": block_volume_config["volume"].get("source_volid", None),
                    "description": block_volume_config["volume"].get("description", None),
                    "snapshot_id": block_volume_config["volume"].get("snapshot_id", None),
                    "backup_id": block_volume_config["volume"].get("backup_id", None),
                    "name": block_volume_config["volume"].get("name", None),
                    "image_id": block_volume_config["volume"].get("imageRef", None),
                    "volume_type": block_volume_config["volume"].get("volume_type", None),
                    "network": block_volume_config["volume"].get("networks", None),
                    "metadata": block_volume_config["volume"].get("metadata", None),
                    "consistency_group_id": block_volume_config["volume"].get("consistencygroup_id", None),
                    # "scheduler_hints": {}
                })
            # apply infra object
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            # commit user environment using git
            #
            return True
        except Exception as e:
            # rollback git reset
            raise Exception(e)
        
    def delete_volume(self, 
                      project_id: str, 
                      volume_id: str):
        try:
            # tf_resource_type, tf_resource_name lấy từ tfstate file
            with open(f"{self.user_workspace_path}/terraform.tfstate", "r") as f:
                tfstate = json.load(f)
            for resource in tfstate.get('resources', []):
                for instance in resource.get('instances', []):
                    if instance.get('attributes', {}).get('id', "") == volume_id:
                        resource_type = resource.get("type")
                        resource_name = resource.get("name")
                        break
            # delete resource
            self.cloud_infra.delete_resource(
                tf_resource_type=resource_type,
                tf_resource_name=resource_name
            )
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            # commit user environment using git
            #
            return True
        except Exception as e:
            # rollback git reset
            raise Exception(e)