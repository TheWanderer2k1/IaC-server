import json
from .schemas import BlockVolumeCreateRequest, VolumeAttachRequest, VolumeDetachRequest
from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from fastapi import Request
from app.config import settings
from pathlib import Path
from app.base_controller import BaseController
from app.utils.utils import Utils

class BlockVolumeController(BaseController): 
    def __init__(self,
                 request: Request,
                 cloud_infra_creator: CloudInfrastructureCreator,
                 location: dict[str, str]):
        super().__init__(request, cloud_infra_creator, location)

    def create_volume(self, block_volume_create_request: BlockVolumeCreateRequest):
        try:
            # generate infra object
            block_volume_config = block_volume_create_request.model_dump(exclude_none=True)
            self.cloud_infra.add_resource(
                tf_resource_type="openstack_blockstorage_volume_v3",
                tf_resource_name=Utils.normalize_terraform_name(f"openstack_compute_instance_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"), # auto generated name
                tf_resource_values={
                    "size": block_volume_config["volume"].get("size", None),
                    "source_vol_id": block_volume_config["volume"].get("source_volid", None),
                    "description": block_volume_config["volume"].get("description", None),
                    "snapshot_id": block_volume_config["volume"].get("snapshot_id", None),
                    "backup_id": block_volume_config["volume"].get("backup_id", None),
                    "name": block_volume_config["volume"].get("name", None),
                    "image_id": block_volume_config["volume"].get("imageRef", None),
                    "volume_type": block_volume_config["volume"].get("volume_type", None),
                    "metadata": block_volume_config["volume"].get("metadata", None),
                    "consistency_group_id": block_volume_config["volume"].get("consistencygroup_id", None),
                    # "scheduler_hints": {}
                })
            # apply infra object
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
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
                    if instance.get('attributes', {}).get('id', "") == volume_id and \
                        resource.get("type") == 'openstack_blockstorage_volume_v3' :
                        resource_name = resource.get("name")
                        break
            # delete resource
            self.cloud_infra.delete_resource(
                tf_resource_type='openstack_blockstorage_volume_v3',
                tf_resource_name=resource_name
            )
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
            raise Exception(e)
        
class BlockVolumeActionController(BaseController):
    def __init__(self,
                 request: Request,
                 cloud_infra_creator: CloudInfrastructureCreator,
                 location: dict[str, str]):
        super().__init__(request, cloud_infra_creator, location)

    def attach_volume(self, 
                      project_id,
                      volume_id,
                      volume_attach_request: VolumeAttachRequest):
        # try:
        #     volume_attach_config = volume_attach_request.model_dump(exclude_none=True)
        #     self.cloud_infra.add_resource(
        #         tf_resource_type="",
        #         tf_resource_name=f"",
        #         tf_resource_values={
                    
        #         }
        #     )
        #     # apply infra object
        #     self.cloud_infra.output_infrastructure()
        #     self.cloud_infra.apply_infrastructure()
        #     # commit user environment using git
        #     #
        #     return True
        # except Exception as e:
        #     # rollback git reset
        #     raise Exception(e)
        pass

    def detach_volume(self,
                      project_id,
                      volume_id,
                      volume_detach_request: VolumeDetachRequest):
        pass
        