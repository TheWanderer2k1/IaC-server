import json
from .schemas import ServerCreateRequest, ServerUpdateRequest, ServerCreateImageRequest
from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from app.config import settings
from fastapi import Request
from pathlib import Path

class ServerController:
    def __init__(self, 
                 request: Request,
                 cloud_infra_creator: CloudInfrastructureCreator,
                 location: dict[str, str]):
        self.cloud_infra_creator = cloud_infra_creator
        self.location = location
        self.user_workspace_path = settings.workspace_basedir + f"/{location.get("domain")}/{location.get("project")}/{location.get("username")}"
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
            auth_url=f"{settings.openstack_config.get("endpoints", "").get("identity", "")}",
            region=f"{location.get("region")}",
            token=request.headers.get("X-Subject-Token"),
            tenant_name=f"{location.get("project")}"
        )

    def list_servers(self):
        pass

    def create_server(self, server_create_request: ServerCreateRequest):
        try:
            # generate infra object
            server_config = server_create_request.model_dump(exclude_none=True)
            self.cloud_infra.add_resource(
                tf_resource_type="openstack_compute_instance_v2",
                tf_resource_name=f"openstack_compute_instance_v2_{self.location.get('domain')}_{self.location.get('project')}_{self.location.get('username')}_dwadad", # auto generated name
                tf_resource_values={
                    "name": server_config["server"].get("name", None),
                    "image_id": server_config["server"].get("imageRef", None),
                    "flavor_id": server_config["server"].get("flavorRef", None),
                    "key_pair": server_config["server"].get("key_name", None),
                    "security_groups": server_config["server"].get("security_groups", None),
                    "user_data": server_config["server"].get("user_data", None),
                    "metadata": server_config["server"].get("metadata", None),
                    # "stop_before_destroy": server_create_request["server"].stop_before_destroy,
                    # "force_delete": server_create_request["server"].force_delete,
                    # "power_state": server_create_request["server"].power_state,
                    "tags": server_config["server"].get("tags", None),
                    # "vendor_options": server_create_request["server"].vendor_options,
                    "network": server_config["server"].get("networks", None),
                    "block_device": server_config["server"].get("block_device_mapping_v2", None),
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

    def create_multiple_servers():
        pass

    def list_servers_detail():
        pass

    def get_server(server_id: str):
        pass

    def update_server(server_id: str, server: ServerUpdateRequest):
        pass

    def delete_server(self, server_id: str):
        try:
            # tf_resource_type, tf_resource_name lấy từ tfstate file
            with open(f"{self.user_workspace_path}/terraform.tfstate", "r") as f:
                tfstate = json.load(f)
            for resource in tfstate.get('resources', []):
                for instance in resource.get('instances', []):
                    if instance.get('attributes', {}).get('id', "") == server_id:
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

class ServerActionController:
    def add_security_group(server_id: str, addSecurityGroup: dict[str, str]):
        pass

    def change_password(server_id: str, changePassword: dict[str, str]):
        pass

    def create_backup(server_id: str, createBackup: dict[str, str]):
        pass

    def create_image(server_id: str, createImage: ServerCreateImageRequest):
        pass

    def lock(server_id: str, lock: dict[str, str] | None = None):
        pass

    def pause(server_id: str, pause: None = None):
        pass

    def reboot(server_id: str, reboot: dict[str, str]):
        pass

    def rebuild():
        pass

    def remove_security_group():
        pass

    def rescue():
        pass

    def resize():
        pass

    def resume():
        pass

    def revert_resize():
        pass

    def os_start():
        pass

    def os_stop():
        pass

    def suspend():
        pass

    def unlock():
        pass

    def unpause():
        pass

    def unrescue():
        pass

    def force_delete():
        pass

    def restore():
        pass

    def os_get_console_output():
        pass

    def shelve():
        pass

    def shelve_offload():
        pass

    def unshelve():
        pass

    def trigger_crash_dump():
        pass