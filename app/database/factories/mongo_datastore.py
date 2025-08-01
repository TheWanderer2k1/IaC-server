from app.config import mongo_conn
from pymongo import MongoClient
from app.database.interfaces.datastore_interface import IDatastore

class MongoDatastore(IDatastore):
    def __init__(self):
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
        """Insert data into a specified collection."""
        return self.db[collection].insert_one(data)

    def find(self, collection: str, query: dict):
        """Find documents in a specified collection based on a query."""
        return list(self.db[collection].find(query))

    def update(self, collection: str, query: dict, update_data: dict):
        """Update documents in a specified collection based on a query."""
        return self.db[collection].update_many(query, {'$set': update_data}, upsert=True)

    def delete(self, collection: str, query: dict):
        """Delete documents from a specified collection based on a query."""
        return self.db[collection].delete_many(query)