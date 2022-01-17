import datetime
from bson.objectid import ObjectId
from typing import Dict
from abc import ABCMeta, abstractmethod
from injector import inject
from app.core.exception import EntityNotFoundException
from app.core.mongo_manager import MongoManager
from .base_entity import BaseEntity


class Repository(metaclass=ABCMeta):
    @inject
    def __init__(self, mongo: MongoManager):
        self.mongo = mongo

    def get_collection(self):
        return self.mongo.get_collection(self.get_collection_name())

    def get_by_id(self, id):
        id = id if isinstance(id, ObjectId) else ObjectId(id)
        return self.get({"_id": id})

    def get(self, criteries: Dict, raise_exception=True):
        data = self.get_collection().find_one(criteries)
        if not data and raise_exception:
            raise EntityNotFoundException
        if not data:
            return
        return self.create_entity(**data)

    def find(self, criteries: Dict):
        list = self.get_collection().find(criteries)
        return [self.create_entity(**data) for data in list]

    def get_or_create(self, criteries: Dict, **kwargs):
        try:
            return self.get(criteries), False
        except EntityNotFoundException:
            entity = self.create_entity(**kwargs)
            return self.insert(entity), True

    def insert(self, entity: BaseEntity):
        data = entity.data
        data["created_at"] = datetime.datetime.now()
        data["updated_at"] = datetime.datetime.now()
        _id = self.get_collection().insert_one(data).inserted_id
        entity._id = _id
        return entity

    def update(self, entity: BaseEntity):
        data = entity.data
        data["updated_at"] = datetime.datetime.now()
        self.get_collection().update_one({"_id": data["_id"]}, {"$set": data})
        return entity

    def save(self, entity: BaseEntity):
        if hasattr(entity, "_id"):
            return self.update(entity)
        return self.insert(entity)

    @abstractmethod
    def get_collection_name(self):
        pass

    @abstractmethod
    def create_entity(self, **kwargs):
        pass
