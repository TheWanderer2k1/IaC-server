from app.base_controller import BaseController
from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from fastapi import Request
from app.utils.utils import Utils
from .schemas import ImportRequest

class ImportController(BaseController):
    def __init__(self, 
                 request: Request,
                 cloud_infra_creator: CloudInfrastructureCreator,
                 location: dict[str, str]):
        super().__init__(request, cloud_infra_creator, location)

    def import_network(self, import_request: ImportRequest):
        config = import_request.model_dump(exclude_none=True)
        return super().import_resource(resource_type="openstack_networking_network_v2",
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_network_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_id=config.get("resource_id"))
    
    def import_subnet(self, import_request: ImportRequest):
        config = import_request.model_dump(exclude_none=True)
        return super().import_resource(resource_type="openstack_networking_subnet_v2", 
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_subnet_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_id=config.get("resource_id"))
    
    def import_router(self, import_request: ImportRequest):
        config = import_request.model_dump(exclude_none=True)
        return super().import_resource(resource_type="openstack_networking_router_v2", 
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_router_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_id=config.get("resource_id"))
    
    def import_router_interface(self, import_request: ImportRequest):
        config = import_request.model_dump(exclude_none=True)
        return super().import_resource(resource_type="openstack_networking_router_interface_v2", 
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_router_interface_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_id=config.get("resource_id"))
    
    def import_port(self, import_request: ImportRequest):
        config = import_request.model_dump(exclude_none=True)
        return super().import_resource(resource_type="openstack_networking_port_v2", 
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_port_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_id=config.get("resource_id"))
    
    def import_floatingip(self, import_request: ImportRequest):
        config = import_request.model_dump(exclude_none=True)
        return super().import_resource(resource_type="openstack_networking_floatingip_v2", 
                                       resource_name=Utils.normalize_terraform_name(f"openstack_networking_floatingip_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_id=config.get("resource_id"))
    
    def import_blockvol(self, import_request: ImportRequest):
        config = import_request.model_dump(exclude_none=True)
        return super().import_resource(resource_type="openstack_blockstorage_volume_v3", 
                                       resource_name=Utils.normalize_terraform_name(f"openstack_blockstorage_volume_v3_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_id=config.get("resource_id"))

    def import_server(self, import_request: ImportRequest):
        config = import_request.model_dump(exclude_none=True)
        return super().import_resource(resource_type="openstack_compute_instance_v2", 
                                       resource_name=Utils.normalize_terraform_name(f"openstack_compute_instance_v2_{self.location.get('project')}_{self.location.get('username')}_{Utils.generate_random_string(5)}"),
                                       resource_id=config.get("resource_id"))
    
    