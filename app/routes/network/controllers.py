import json
from .schemas import NetworkCreateRequest, SubnetCreateRequest, RouterCreateRequest, AddInterfaceRouterRequest, PortCreateRequest, NetworkUpdateRequest, SubnetUpdateRequest
from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from app.config import settings
from app.base_controller import BaseController
from fastapi import Request
from pathlib import Path
from app.utils.utils import Utils

class NetworkController(BaseController):
    def __init__(self, 
                 request: Request,
                 cloud_infra_creator: CloudInfrastructureCreator,
                 location: dict[str, str]):
        super().__init__(request, cloud_infra_creator, location)

    def create_network(self, network_create_request: NetworkCreateRequest):
        network_config = network_create_request.model_dump(exclude_none=True)
        return super().create_resource(resource_type="openstack_networking_network_v2",
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_network_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_value={
                                            "name": network_config["network"].get("name", None),
                                            "description": network_config["network"].get("description", None),
                                            "shared": network_config["network"].get("shared", None),
                                            # "external": network_config["network"].get("external", None),
                                            "tenant_id": network_config["network"].get("tenant_id", None),
                                            "admin_state_up": network_config["network"].get("admin_state_up", None),
                                            # "segments": network_config["network"].get("segments", None),
                                            # "value_specs": network_config["network"].get("value_specs", None),
                                            "availability_zone_hints": network_config["network"].get("availability_zone_hints", None),
                                            # "tags": network_config["network"].get("tags", None),
                                            "transparent_vlan": network_config["network"].get("vlan_transparent", None),
                                            "port_security_enabled": network_config["network"].get("port_security_enabled", None),
                                            "mtu": network_config["network"].get("mtu", None),
                                            "dns_domain": network_config["network"].get("dns_domain", None),
                                            "qos_policy_id": network_config["network"].get("qos_policy_id", None),
                                        })
    
    def update_network(self, network_id: str, network_update_request: NetworkUpdateRequest):
        network_config = network_update_request.model_dump(exclude_none=True)
        return super().modify_resource(resource_type="openstack_networking_network_v2",
                                       resource_id=network_id,
                                       resource_values={
                                            "name": network_config["network"].get("name", None),
                                            "description": network_config["network"].get("description", None),
                                            "admin_state_up": network_config["network"].get("admin_state_up", None),
                                            "transparent_vlan": network_config["network"].get("vlan_transparent", None),
                                            "shared": network_config["network"].get("shared", None),
                                            "port_security_enabled": network_config["network"].get("port_security_enabled", None),
                                            "dns_domain": network_config["network"].get("dns_domain", None),
                                       })
        
    def delete_network(self, network_id: str):
        return super().delete_resource(resource_type="openstack_networking_network_v2", 
                                       resource_id=network_id)
    
    def create_subnet(self, subnet_create_request: SubnetCreateRequest):
        subnet_config = subnet_create_request.model_dump(exclude_none=True)
        return super().create_resource(resource_type="openstack_networking_subnet_v2",
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_subnet_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_value={
                                            "network_id": subnet_config["subnet"].get("network_id", None),
                                            "cidr": subnet_config["subnet"].get("cidr", None),
                                            "prefix_length": subnet_config["subnet"].get("prefix_length", None),
                                            "ip_version": subnet_config["subnet"].get("ip_version", None),
                                            "ipv6_address_mode": subnet_config["subnet"].get("ipv6_address_mode", None),
                                            "ipv6_ra_mode": subnet_config["subnet"].get("ipv6_ra_mode", None),
                                            "name": subnet_config["subnet"].get("name", None),
                                            "description": subnet_config["subnet"].get("description", None),
                                            "tenant_id": subnet_config["subnet"].get("tenant_id", None),
                                            "allocation_pool": subnet_config["subnet"].get("allocation_pool", None),
                                            "gateway_ip": subnet_config["subnet"].get("gateway_ip", None),
                                            # "no_gateway": subnet_config["subnet"].get("no_gateway", None),
                                            "enable_dhcp": subnet_config["subnet"].get("enable_dhcp", None),
                                            "dns_nameservers": subnet_config["subnet"].get("dns_nameservers", None),
                                            "dns_publish_fixed_ip": subnet_config["subnet"].get("dns_publish_fixed_ip", None),
                                            "service_types": subnet_config["subnet"].get("service_types", None),
                                            "segment_id": subnet_config["subnet"].get("segment_id", None),
                                            "subnetpool_id": subnet_config["subnet"].get("subnetpool_id", None),
                                            # "value_specs": subnet_config["subnet"].get("value_specs", None),
                                            # "tags": subnet_config["subnet"].get("tags", None),
                                       })
    
    def update_subnet(self, subnet_id: str, subnet_update_request: SubnetUpdateRequest):
        subnet_config = subnet_update_request.model_dump(exclude_none=True)
        return super().modify_resource(resource_type="openstack_networking_subnet_v2",
                                       resource_id=subnet_id,
                                       resource_values={
                                            "name": subnet_config["subnet"].get("name", None),
                                            "description": subnet_config["subnet"].get("description", None),
                                            "allocation_pool": subnet_config["subnet"].get("allocation_pool", None),
                                            "gateway_ip": subnet_config["subnet"].get("gateway_ip", None),
                                            "enable_dhcp": subnet_config["subnet"].get("enable_dhcp", None),
                                            "dns_nameservers": subnet_config["subnet"].get("dns_nameservers", None),
                                            "service_types": subnet_config["subnet"].get("service_types", None),
                                       })
    
    def delete_subnet(self, subnet_id: str):
        return super().delete_resource(resource_type="openstack_networking_subnet_v2",
                                       resource_id=subnet_id)
    
    def create_router(self, router_create_request: RouterCreateRequest):
        router_config = router_create_request.model_dump(exclude_none=True)
        return super().create_resource(resource_type="openstack_networking_router_v2",
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_router_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_value={
                                            "tenant_id": router_config["router"].get("tenant_id", None),
                                            "name": router_config["router"].get("name", None),
                                            "description": router_config["router"].get("name", None),
                                            "admin_state_up": router_config["router"].get("admin_state_up", None),
                                            "distributed": router_config["router"].get("distributed", None),
                                            "external_network_id": router_config["router"].get("external_gateway_info", None).get("network_id", None),
                                            "enable_snat": router_config["router"].get("external_gateway_info", None).get("enable_snat", None),
                                            "external_fixed_ip": router_config["router"].get("external_gateway_info", None).get("external_fixed_ips", None),
                                            "external_qos_policy_id": router_config["router"].get("external_gateway_info", None).get("qos_policy_id", None),
                                            # "external_subnet_ids": router_config["router"].get("external_subnet_ids", None),
                                            # "value_specs": router_config["router"].get("value_specs", None),
                                            # "tags": router_config["router"].get("tags", None),
                                            # "vendor_options": router_config["router"].get("vendor_option", None),
                                            # "availability_zone_hints": router_config["router"].get("availability_zone_hints", None),
                                       })

    def delete_router(self, router_id: str):
        return super().delete_resource(resource_type="openstack_networking_router_v2",
                                       resource_id=router_id)      

    def add_interface_to_router(self,
                                router_id: str, 
                                add_interface_to_router: AddInterfaceRouterRequest):
        config = add_interface_to_router.model_dump(exclude_none=True)
        return super().create_resource(resource_name="openstack_networking_router_interface_v2",
                                       resource_type=Utils.normalize_terraform_name(f"openstack_networking_router_interface_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_value={
                                           "router_id": router_id,
                                           "subnet_id": config.get("subnet_id", None),
                                           "port_id": config.get("port_id", None),
                                        #    "force_destroy": config.get("force_destroy", None),
                                       })
    
    def remove_interface_from_router(self,
                                     router_id: str,
                                     add_interface_to_router: AddInterfaceRouterRequest):
        try:
            config = add_interface_to_router.model_dump(exclude_none=True)
            # tf_resource_type, tf_resource_name lấy từ tfstate file
            with open(f"{self.user_workspace_path}/terraform.tfstate", "r") as f:
                tfstate = json.load(f)
            for resource in tfstate.get('resources', []):
                for instance in resource.get('instances', []):
                    if instance.get('attributes', {}).get('router_id', "") == router_id and \
                        ((instance.get('attributes', {}).get('subnet_id', "") and instance.get('attributes', {}).get('subnet_id', "") == config.get("subnet_id", None)) or
                        (instance.get('attributes', {}).get('port_id', "") and instance.get('attributes', {}).get('port_id', "") == config.get("port_id", None))) and \
                        resource.get("type") == "openstack_networking_router_interface_v2" :
                        resource_name = resource.get("name")
                        break
            # delete resource
            self.cloud_infra.delete_resource(
                tf_resource_type="openstack_networking_router_interface_v2",
                tf_resource_name=resource_name
            )
            self.cloud_infra.output_infrastructure()
            self.cloud_infra.apply_infrastructure()
            return True
        except Exception as e:
            raise Exception(e)
        
    def create_port(self, port_create_request: PortCreateRequest):
        port_config = port_create_request.model_dump(exclude_none=True)
        return super().create_resource(resource_type="openstack_networking_port_v2",
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_port_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_value={
                                            "name": port_config["port"].get("name", None),
                                            "description": port_config["port"].get("description", None),
                                            "network_id": port_config["port"].get("network_id"),
                                            "admin_state_up": port_config["port"].get("admin_state_up", None),
                                            "mac_address": port_config["port"].get("mac_address", None),
                                            "tenant_id": port_config["port"].get("tenant_id", None),
                                            "device_owner": port_config["port"].get("device_owner", None),
                                            "security_group_ids": port_config["port"].get("security_groups", None),
                                            # "no_security_groups": port_config["port"].get("no_security_groups", None),
                                            "device_id": port_config["port"].get("device_id", None),
                                            "fixed_ip": port_config["port"].get("fixed_ips", None),
                                            # "no_fixed_ip": port_config["port"].get("no_fixed_ip", None),
                                            "allowed_address_pairs": port_config["port"].get("allowed_address_pairs", None),
                                            "extra_dhcp_option": port_config["port"].get("extra_dhcp_opts", None),
                                            "port_security_enabled": port_config["port"].get("port_security_enabled", None),
                                            # "value_specs": port_config["port"].get("value_specs", None),
                                            "tags": port_config["port"].get("tags", None),
                                            # "binding": port_config["port"].get("binding", None),
                                            "dns_name": port_config["port"].get("dns_name", None),
                                            "qos_policy_id": port_config["port"].get("qos_policy_id", None),
                                       })
    
    def delete_port(self, port_id: str):
        return super().delete_resource(resource_type="openstack_networking_port_v2",
                                       resource_id=port_id)