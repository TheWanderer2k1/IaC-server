from abc import ABC, abstractmethod

class IDatastore(ABC):
    @abstractmethod
    def connect(self):
        """Establish a connection to the datastore."""
        pass

    @abstractmethod
    def disconnect(self):
        """Close the connection to the datastore."""
        pass

    @abstractmethod
    def insert(self, collection: str, data: dict):
        """Insert data into a specified collection."""
        pass

    @abstractmethod
    def find(self, collection: str, query: dict):
        """Find documents in a specified collection based on a query."""
        pass

    @abstractmethod
    def update(self, collection: str, query: dict, update_data: dict):
        """Update documents in a specified collection based on a query."""
        pass

    @abstractmethod
    def delete(self, collection: str, query: dict):
        """Delete documents from a specified collection based on a query."""
        pass