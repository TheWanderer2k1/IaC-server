from abc import ABC, abstractmethod
from app.database.interfaces.datastore_interface import IDatastore

class DatastoreCreator(ABC):
    @abstractmethod
    def create_datastore(self) -> IDatastore:
        """Create and return an instance of a datastore."""
        pass