from app.services.api.user import UserApiService
from injector import inject
from app.core.mongo_manager import MongoManager
from app.models.entities import User
from ..repository import Repository

TELEGRAM_ID_FIELD = "telegram_id"


class UserRepository(Repository):
    @inject
    def __init__(self, mongo: MongoManager, user_service: UserApiService):
        super().__init__(mongo=mongo)
        self.user_service = user_service

    def get_collection_name(self):
        return "users"

    def create_entity(self, **kwargs):
        return User(**kwargs)

    def get_by_telegram_id(self, id):
        return self.get({TELEGRAM_ID_FIELD: id})

    def get_or_create_user(self, external_id, criteries, data):
        entity, created = self.get_or_create(criteries, **data)
        if created:
            user_backend = self.user_service.get_or_create(
                external_id=external_id, data=data
            )
            entity.backend_id = user_backend["id"]
            self.save(entity)
        else:
            changed = False
            for key, value in data.items():
                if getattr(entity, key) != value:
                    changed = True
                    setattr(entity, key, value)
            if changed:
                user_backend = self.user_service.get_or_create(
                    external_id=external_id, data=data
                )
                self.save(entity)
        return entity
