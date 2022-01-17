from pymongo import MongoClient
from injector import inject
from app.config import Config


class MongoManager:
    @inject
    def __init__(self, config: Config):
        self.config = config
        self.client = MongoClient(self.config.MONGO_CONECTION)
        self.database = self.client[self.config.DATABASE]

    def get_db(self):
        return self.database

    def get_collection(self, collection_name):
        return self.database[collection_name]
