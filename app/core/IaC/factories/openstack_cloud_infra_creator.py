from app.core.IaC.abstracts.cloud_infra_creator import CloudInfrastructureCreator
from .openstack_cloud_infra import OpenStackCloudInfrastructure

class OpenStackCloudInfrastructureCreator(CloudInfrastructureCreator):
    def create_infrastructure(self, path_to_tf_workspace: str, **kwargs) -> OpenStackCloudInfrastructure:
        """Create an OpenStack cloud infrastructure instance."""
        try:
            if not path_to_tf_workspace:
                raise ValueError("Path to Terraform workspace cannot be empty.")
            # use token instead of user_name and password
            if "provider_version" not in kwargs or \
                "auth_url" not in kwargs or \
                "region" not in kwargs or \
                "token" not in kwargs or \
                "tenant_name" not in kwargs:
                 raise ValueError("Missing required OpenStack authentication parameters.")
                
            return OpenStackCloudInfrastructure(path_to_tf_workspace,
                                                provider_version=kwargs["provider_version"], 
                                                auth_url=kwargs["auth_url"],
                                                region=kwargs["region"],
                                                token=kwargs["token"],  # Use token for authentication
                                                tenant_name=kwargs["tenant_name"])
        except Exception as e:
            print(f"An error occurred while creating OpenStack cloud infrastructure: {e}")
            raise e

oc_creator = OpenStackCloudInfrastructureCreator()