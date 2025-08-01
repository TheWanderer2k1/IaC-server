from .mongo_datastore import MongoDatastore
from app.database.abstracts.datastore_creator import DatastoreCreator

class MongoDatastoreCreator(DatastoreCreator):
    def create_datastore(self) -> MongoDatastore:
        """Create and return an instance of MongoDatastore."""
        return MongoDatastore()
    
mongo_creator = MongoDatastoreCreator()