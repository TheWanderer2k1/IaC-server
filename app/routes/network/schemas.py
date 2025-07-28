from pydantic import Field, model_validator, AliasChoices
from app.base_schema import BaseSchema

class Network(BaseSchema):
    admin_state_up: bool | None = None
    dns_domain: str | None = None
    mtu: int | None = None
    name: str | None = None
    port_security_enabled: bool | None = None
    network_type: str | None = Field(default=None, validation_alias=AliasChoices("provider:network_type"))
    physical_network: str | None = Field(default=None, validation_alias=AliasChoices("provider:physical_network"))
    segmentation_id: int | None = Field(default=None, validation_alias=AliasChoices("provider:segmentation_id"))
    qos_policy_id: str | None = None 
    router_external: bool | None = Field(default=None, validation_alias=AliasChoices("router:external"))
    # segments: list[segment] | None = None
    shared: bool | None = None
    tenant_id: str | None = None
    vlan_transparent: bool | None = None
    description: str | None = None
    is_default: bool | None = None
    availability_zone_hints: list[str] | None = None

class NetworkCreateRequest(BaseSchema):
    network: Network

class NetworkUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None
    admin_state_up: bool | None = None
    vlan_transparent: bool | None = None
    port_security_enabled: bool | None = None
    dns_domain: str | None = None
    shared: bool | None = None

class NetworkUpdateRequest(BaseSchema):
    network: NetworkUpdate

class Subnet(BaseSchema):
    tenant_id: str | None = None
    project_id: str | None = None
    name: str | None = None
    description: str | None = None
    enable_dhcp: bool | None = None
    network_id: str
    dns_nameservers: list[str] | None = None
    allocation_pools: dict[str, str] | None = None
    host_routes: list[str] | None = None
    ip_version: int | None = None
    gateway_ip: str | None = None
    cidr: str
    prefixlen: int | None = None
    ipv6_address_mode: str | None = None
    ipv6_ra_mode: str | None = None
    segment_id: str | None = None
    subnetpool_id: str | None = None
    user_default_subnetpool: bool | None = None
    service_types: list[str] | None = None
    dns_publish_fixed_ip: bool | None = None

class SubnetCreateRequest(BaseSchema):
    subnet: Subnet

class SubnetUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None
    enable_dhcp: bool | None = None
    allocation_pools: dict[str, str] | None = None
    dns_nameservers: list[str] | None = None
    gateway_ip: str | None = None
    service_types: list[str] | None = None

class SubnetUpdateRequest(BaseSchema):
    subnet: SubnetUpdate

class ExternalFixedIp(BaseSchema):
    subnet_id: str | None = None
    ip_address: str | None = None

class ExternalGatewayInfo(BaseSchema):
    network_id: str
    enable_snat: bool | None = None
    external_fixed_ips: ExternalFixedIp | None = None
    qos_policy_id: str | None = None

class Router(BaseSchema):
    tenant_id: str | None = None
    project_id: str | None = None
    name: str | None = None
    description: str | None = None
    admin_state_up: bool | None = None
    external_gateway_info: ExternalGatewayInfo | None = None
    distributed: bool | None = None
    ha: bool | None = None
    availability_zone_hints: list[str] | None = None
    service_type_id: str | None = None
    flavor_id: str | None = None
    enable_ndp_proxy: bool | None = None
    enable_default_route_bfd: bool | None = None
    enable_default_route_ecmp: bool | None = None

class RouterCreateRequest(BaseSchema):
    router: Router

class AddInterfaceRouterRequest(BaseSchema):
    subnet_id: str | None = None
    port_id: str | None = None

class PortFixedIp(BaseSchema):
    subnet_id: str | None = None
    ip_address: str | None = None

class PortAllowedAddressPair(BaseSchema):
    ip_address: str
    mac_address: str | None = None

class PortExtraDHCPOpts(BaseSchema):
    name: str
    value: str
    ip_version: str | None = None

class Port(BaseSchema):
    admin_state_up: bool | None = None
    allowed_address_pairs: list[PortAllowedAddressPair] | None = None
    # binding_host_id: str | None = Field(default=None, validation_alias=AliasChoices("binding:host_id"))
    # binding_profile: 
    # binding_vnic_type: str | None = Field(default=None, validation_alias=AliasChoices("binding:vnic_type"))
    description: str | None = None
    device_id: str | None = None
    device_owner: str | None = None
    dns_domain: str | None = None
    dns_name: str | None = None
    extra_dhcp_opts: PortExtraDHCPOpts | None = None
    fixed_ips: list[PortFixedIp] | None = None
    # hints:
    mac_address: str | None = None
    name: str | None = None
    network_id: str
    numa_affinity_policy: str | None = None
    port_security_enabled: bool | None = None
    project_id: str | None = None
    qos_policy_id: str | None = None
    security_groups: list[str] | None = None
    tenant_id: str | None = None
    propagate_uplink_status: bool | None = None
    mac_learning_enabled: bool | None = None
    port_trusted_vif: bool | None = None

class PortCreateRequest(BaseSchema):
    port: Port
