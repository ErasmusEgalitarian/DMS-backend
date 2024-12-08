from pymongo import MongoClient

import constants


class MongoConnector:
    def __init__(self):
        self._connection_string = constants.mongo_connection_string
        self.client = MongoClient(self._connection_string)

        self.database = self.get_database()

    def get_database(self):
        return self.client[constants.mongo_database_name]

    def insert_documents(self, collection_name, items):
        collection = self.database[collection_name]
        collection.insert_many(items)
