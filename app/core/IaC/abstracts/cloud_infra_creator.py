from abc import ABC, abstractmethod
from app.core.IaC.interfaces.cloud_infra_interface import ICloudInfrastructure

class CloudInfrastructureCreator(ABC):
    """Abstract base class for creating cloud infrastructure instances."""
    @abstractmethod
    def create_infrastructure(self, path_to_tf_workspace: str, **kwargs) -> ICloudInfrastructure:
        """Create a cloud infrastructure instance."""
        pass