from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from app.base_controller import BaseController
from fastapi import Request
from .schemas import InfraPreset1Request
from app.utils.utils import Utils
import json
from app.exceptions.controller_exception import ControllerException
import time

class InfraController(BaseController):
    def __init__(self, 
                 request: Request,
                 cloud_infra_creator: CloudInfrastructureCreator,
                 location: dict[str, str]):
        super().__init__(request, cloud_infra_creator, location)

    def provision_infra_vdi(self, infra_preset1_request: InfraPreset1Request):
        try:
            config = infra_preset1_request.model_dump(exclude_none=True)
            # defind resource name in config file
            network_name = Utils.normalize_terraform_name(f"openstack_networking_network_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}")
            subnet_name = Utils.normalize_terraform_name(f"openstack_networking_subnet_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}")
            router_name = Utils.normalize_terraform_name(f"openstack_networking_router_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}")
            router_interface_name = Utils.normalize_terraform_name(f"openstack_networking_router_interface_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}")
            block_vol_name = Utils.normalize_terraform_name(f"openstack_blockstorage_volume_v3_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}")
            port_name = Utils.normalize_terraform_name(f"openstack_networking_port_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}")
            server_name = Utils.normalize_terraform_name(f"openstack_compute_instance_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}")
            floating_ip_name = Utils.normalize_terraform_name(f"openstack_networking_floatingip_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}")
            # add network
            self.cloud_infra.add_resource(
                resource_type="openstack_networking_network_v2",
                resource_name=network_name,
                resource_values={
                    "name": f"network_{Utils.generate_random_string(5)}",
                    "admin_state_up": True
                }
            )
            # add subnet
            self.cloud_infra.add_resource(
                resource_type="openstack_networking_subnet_v2",
                resource_name=subnet_name,
                resource_values={
                    "name": f"subnet_{Utils.generate_random_string(5)}",
                    "network_id": "${openstack_networking_network_v2." + network_name + ".id}",
                    "cidr": config.get("subnet_cidr"),
                    "ip_version": "4"
                }
            )
            # add router
            self.cloud_infra.add_resource(
                resource_type="openstack_networking_router_v2",
                resource_name=router_name,
                resource_values={
                    "name": f"router_{Utils.generate_random_string(5)}",
                    "admin_state_up": True,
                    "external_network_id": "10f06942-af56-4bfc-a76a-8ea288625e84"
                }
            )
            # add router interface
            self.cloud_infra.add_resource(
                resource_type="openstack_networking_router_interface_v2",
                resource_name=router_interface_name,
                resource_values={
                    "router_id": "${openstack_networking_router_v2." + router_name + ".id}",
                    "subnet_id": "${openstack_networking_subnet_v2." + subnet_name + ".id}"
                }
            )
            # add block volume
            self.cloud_infra.add_resource(
                resource_type="openstack_blockstorage_volume_v3",
                resource_name=block_vol_name,
                resource_values={
                    "description": "bootable volume",
                    # "image_id": config.get("image_id"),
                    "source_vol_id": "ed6a5f0f-beff-4177-89eb-e1f261963e14",
                    "name": f"block_vol_{Utils.generate_random_string(5)}",
                    # "volume_type": "HDD-phase3",
                    "size": config.get("vol_size"),
                }
            )
            # add port
            self.cloud_infra.add_resource(
                resource_type="openstack_networking_port_v2",
                resource_name=port_name,
                resource_values={
                    "network_id": "${openstack_networking_network_v2." + network_name + ".id}",
                    "name": f"port_{Utils.generate_random_string(5)}",
                    "admin_state_up": True,
                    "fixed_ip": {
                        "subnet_id": "${openstack_networking_subnet_v2." + subnet_name + ".id}"
                    }
                }
            )
            # add server
            self.cloud_infra.add_resource(
                resource_type="openstack_compute_instance_v2",
                resource_name=server_name,
                resource_values={
                    "block_device": [
                        {
                            "boot_index": 0,
                            "destination_type": "volume",
                            "source_type": "volume",
                            "uuid": "${openstack_blockstorage_volume_v3." + block_vol_name + ".id}"
                        }
                    ],
                    "flavor_id": config.get("flavor_id"),
                    "name": f"server_{Utils.generate_random_string(5)}",
                    "network": [
                        {
                        "port": "${openstack_networking_port_v2." + port_name + ".id}"
                        }
                    ],
                    "security_groups": [
                        "default"
                    ]
                }
            )
            # # add floating ip
            # self.cloud_infra.add_resource(
            #     resource_type="openstack_networking_floatingip_v2",
            #     resource_name=floating_ip_name,
            #     resource_values={
            #         "pool": "provider",
            #         "port_id": "${openstack_networking_port_v2." + port_name + ".id}"
            #     }
            # )
            # apply
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            # read from terrfarm state
            with open(f"{self.user_workspace_path}/terraform.tfstate", 'r') as f:
                state = json.load(f)
            created_resources = []
            for resource in state.get('resources', []):
                if resource['name'] == network_name or \
                   resource['name'] == subnet_name or \
                   resource['name'] == router_name or \
                   resource['name'] == router_interface_name or \
                   resource['name'] == block_vol_name or \
                   resource['name'] == port_name or \
                   resource['name'] == server_name:
                #    resource['name'] == floating_ip_name:
                    created_resources.append(resource)
            # return the created resources
            return created_resources
        except Exception as e:
            raise ControllerException(f"An error occurred while provisioning infrastructure preset 1: {e}")
        
    @staticmethod
    def delayed_response():
        try:
            print("Starting delay...")
            time.sleep(10) 
            print("Response after delay")
            return "Return some data after delay"
        except Exception as e:
            raise ControllerException(f"An error occurred in the test route: {e}")