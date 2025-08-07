from app.config import settings
from pymongo import MongoClient
from app.database.interfaces.datastore_interface import IDatastore
from app.exceptions.datastore_exception import DatastoreOperationException

class MongoDatastore(IDatastore):
    def __init__(self):
        mongo_conn = settings.mongo_conn
        self.client = MongoClient(mongo_conn['host'], mongo_conn['port'])
        self.db = self.client[mongo_conn.get('db_name', 'default_db')]

    def connect(self):
        """Not implemented yet."""
        pass
        

    def disconnect(self):
        """Close the connection to the MongoDB datastore."""
        if self.client:
            self.client.close()

    def insert(self, collection: str, data: dict):
        try:
            """Insert data into a specified collection."""
            return self.db[collection].insert_one(data)
        except Exception as e:
            raise DatastoreOperationException(f"Failed to insert data into {collection}: {e}")

    def find(self, collection: str, query: dict):
        try:
            """Find documents in a specified collection based on a query."""
            return list(self.db[collection].find(query))
        except Exception as e:
            raise DatastoreOperationException(f"Failed to find data in {collection}: {e}")

    def update(self, collection: str, query: dict, update_data: dict):
        try:
            """Update documents in a specified collection based on a query."""
            return self.db[collection].update_many(query, {'$set': update_data}, upsert=True)
        except Exception as e:
            raise DatastoreOperationException(f"Failed to update data in {collection}: {e}")

    def delete(self, collection: str, query: dict):
        try:
            """Delete documents from a specified collection based on a query."""
            return self.db[collection].delete_many(query)
        except Exception as e:
            raise DatastoreOperationException(f"Failed to delete data from {collection}: {e}")