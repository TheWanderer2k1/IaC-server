import json
import aiohttp
from .schemas import ServerCreateRequest, ServerUpdateRequest, ServerCreateImageRequest, VolumeAttachmentRequest, RemoteConsoleRequest
from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from app.config import settings
from app.base_controller import BaseController
from fastapi import Request
from pathlib import Path
from app.utils.utils import Utils

class ServerController(BaseController):
    def __init__(self, 
                 request: Request,
                 cloud_infra_creator: CloudInfrastructureCreator,
                 location: dict[str, str]):
        super().__init__(request, cloud_infra_creator, location)

    def list_servers(self):
        pass

    def create_server(self, server_create_request: ServerCreateRequest):
        server_config = server_create_request.model_dump(exclude_none=True)
        return super().create_resource(resource_type="openstack_compute_instance_v2",
                                       resource_name=Utils.normalize_terraform_name(f"openstack_compute_instance_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_values={
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
    
    def update_server(self, server_id: str, server_update_request: ServerUpdateRequest):
        server_config = server_update_request.model_dump(exclude_none=True)
        return super().modify_resource(resource_type="openstack_compute_instance_v2",
                                       resource_id=server_id,
                                       resource_values={
                                           "name": server_config["server"].get("name", None),
                                           "flavor_id": server_config["server"].get("flavor_id", None),
                                           "flavor_name": server_config["server"].get("flavor_name", None),
                                           "security_groups": server_config["server"].get("security_groups", None),
                                           "metadata": server_config["server"].get("metadata", None),
                                           "admin_pass": server_config["server"].get("admin_pass", None),
                                           "stop_before_destroy": server_config["server"].get("stop_before_destroy", None),
                                           "force_delete": server_config["server"].get("force_delete", None),
                                           "power_state": server_config["server"].get("power_state", None),
                                       })

    def create_multiple_servers():
        pass

    def list_servers_detail():
        pass

    def get_server(server_id: str):
        pass

    def delete_server(self, server_id: str):
        return super().delete_resource(resource_type="openstack_compute_instance_v2", 
                                       resource_id=server_id)
    
    async def get_console(self, server_id: str, remote_console_request: RemoteConsoleRequest):
        try:
            config = remote_console_request.model_dump(exclude_none=True)
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{settings.openstack_config.get('endpoints', {}).get('compute', '')}servers/{server_id}/remote-consoles",
                    headers = {
                        "X-Auth-Token": self.token
                    },
                    json = {
                        "remote-console": {
                            "protocol": config.get("remote_console", {}).get("protocol"),
                            "type": config.get("remote_console", {}).get("console_type")
                        }
                    }
                ) as resp:
                    try:
                        response_data = await resp.json()
                    except aiohttp.ContentTypeError:
                        response_data = await resp.text()
                    except json.decoder.JSONDecodeError:
                        response_data = await resp.text()
                    if resp.status != 200:
                        raise Exception(f"Failed to get console: {response_data}")
                    return response_data
        except Exception as e:
            raise Exception(e)

    async def get_novnc_console(self, server_id: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{settings.openstack_config.get('endpoints', {}).get('compute', '')}servers/{server_id}/action",
                    headers = {
                        "X-Auth-Token": self.token
                    },
                    json = {
                        "os-getVNCConsole": {
                            "type": "novnc",
                        }
                    }
                ) as resp:
                    try:
                        response_data = await resp.json()
                    except aiohttp.ContentTypeError:
                        response_data = await resp.text()
                    except json.decoder.JSONDecodeError:
                        response_data = await resp.text()
                    if resp.status != 200:
                        raise Exception(f"Failed to get console: {response_data}")
                    return response_data
        except Exception as e:
            raise Exception(e)
        
    def attach_volume(self,
                      server_id: str,
                      volume_attachment_request: VolumeAttachmentRequest):
        volume_attachment_config = volume_attachment_request.model_dump(exclude_none=True)
        return super().create_resource(resource_type="openstack_compute_volume_attach_v2",
                                       resource_name=Utils.normalize_terraform_name(f"openstack_compute_volume_attach_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_values={
                                            "instance_id": server_id,
                                            "volume_id": volume_attachment_config["volumeAttachment"].get("volumeId"),
                                            "device": volume_attachment_config["volumeAttachment"].get("device", None),
                                            "tag": volume_attachment_config["volumeAttachment"].get("tag", None),
                                        })
        
    def detach_volume(self,
                      server_id: str,
                      volume_id: str):
        try:
            # tf_resource_type, tf_resource_name lấy từ tfstate file
            with open(f"{self.user_workspace_path}/terraform.tfstate", "r") as f:
                tfstate = json.load(f)
            for resource in tfstate.get('resources', []):
                for instance in resource.get('instances', []):
                    if instance.get('attributes', {}).get('instance_id', "") == server_id and \
                        instance.get('attributes', {}).get('volume_id', "") == volume_id and \
                        resource.get("type") == 'openstack_compute_volume_attach_v2' :
                        resource_name = resource.get("name")
                        break
            # delete resource
            self.cloud_infra.delete_resource(
                tf_resource_type='openstack_compute_volume_attach_v2',
                tf_resource_name=resource_name
            )
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
            raise Exception(e)
        
    async def get_flavors(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{settings.openstack_config.get('endpoints', {}).get('compute', '')}flavors/detail", 
                    headers={"X-Auth-Token": self.token}                       
                ) as resp:
                    try:
                        response_data = await resp.json()
                    except aiohttp.ContentTypeError:
                        response_data = await resp.text()
                    except json.decoder.JSONDecodeError:
                        response_data = await resp.text()
                    if resp.status != 200:
                        raise Exception(f"Failed to get flavors: {response_data}")
                    return response_data
        except Exception as e:
            raise Exception(e)

    def add_security_group(self, server_id: str, addSecurityGroup: dict[str, str]):
        pass

    def change_password(self, server_id: str, changePassword: dict[str, str]):
        pass

    def create_backup(self, server_id: str, createBackup: dict[str, str]):
        pass

    def create_image(self, server_id: str, createImage: ServerCreateImageRequest):
        pass

    def lock(self, server_id: str, lock: dict[str, str] | None = None):
        pass

    def pause(self, server_id: str, pause: None = None):
        pass

    def reboot(self, server_id: str, reboot: dict[str, str]):
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