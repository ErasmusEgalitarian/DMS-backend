from bson.objectid import ObjectId

from pymongo import MongoClient

from src import constants


class MongoConnector:
    def __init__(self):
        self._connection_string = constants.env_config.MONGO_CONNECTION_STRING
        self.client = MongoClient(self._connection_string)

        self.database = self.get_database()

    def get_database(self):
        return self.client[constants.env_config.MONGO_DATABASE_NAME]

    def insert_documents(self, collection_name, items):
        collection = self.database[collection_name]
        collection.insert_many(items)

    def get_documents(self, collection_name, query=None):
        collection = self.database[collection_name]
        if query is None:
            return collection.find()
        return collection.find(query)

    def get_by_id(self, collection_name, identifier):
        try:
            doc_id = ObjectId(identifier)
            collection = self.database[collection_name]
            return collection.find_one({'_id': doc_id})
        except:
            print(f'Error getting document from collection {collection_name} with id: {identifier}')
            return None
