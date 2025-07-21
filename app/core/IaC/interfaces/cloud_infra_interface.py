from abc import ABC, abstractmethod

class ICloudInfrastructure(ABC):
    @abstractmethod
    def _refresh_infrastructure(self):
        """Refresh the infrastructure state."""
        pass

    @abstractmethod
    def _construct_infrastructure_dict(self):
        """Construct the infrastructure dictionary from the Terraform state."""
        pass

    @abstractmethod
    def _construct_infrastructure_graph(self):
        """Construct the infrastructure graph from the Terraform state."""
        pass

    @abstractmethod
    def add_resource(self, resource_type, resource_name, **kwargs):
        """Add a resource to the infrastructure."""
        pass

    @abstractmethod
    def modify_resource(self, resource_type, resource_name, **kwargs):
        """Modify an existing resource in the infrastructure."""
        pass

    @abstractmethod
    def delete_resource(self, resource_type, resource_name):
        """Delete a resource from the infrastructure."""
        pass

    @abstractmethod
    def output_infrastructure(self):
        """Output the current state of the infrastructure."""
        pass

    @abstractmethod
    def apply_infrastructure(self):
        """Apply the current state of the infrastructure."""
        pass