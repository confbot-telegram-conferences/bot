from injector import inject
from app.core.mongo_manager import MongoManager


class ClearCollections:
    @inject
    def __init__(self, mongo: MongoManager):
        self.mongo = mongo

    def __call__(self, collections):
        for collection in collections:
            self.mongo.get_collection(collection).drop()
