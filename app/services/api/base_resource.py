from abc import ABCMeta, abstractmethod
from app.models.base_entity import BaseEntity
from app.models.entities.user import User
from injector import inject
from app.request import Request


class BaseResource(metaclass=ABCMeta):
    @inject
    def __init__(self, request: Request) -> None:
        self.request = request

    @abstractmethod
    def create_entity(self, **kwargs):
        pass

    @abstractmethod
    def get_uri(self, **kwargs):
        pass

    def _get_uri(self, **kwargs):
        uri = self.get_uri(**kwargs)
        if isinstance(uri, tuple):
            return uri
        return uri, kwargs

    def get_by_id(self, id, user: User, **kwargs):
        uri, kwargs = self._get_uri(**kwargs)
        response = self.request.get(
            f"{uri}{id}/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            **kwargs,
        )
        return self.create_entity(**response.json())

    def list(self, user: User, **kwargs):
        uri, kwargs = self._get_uri(**kwargs)
        response = self.request.get(
            uri,
            headers=self.request.get_user_headers(user_id=user.backend_id),
            **kwargs,
        )
        data = response.json()
        return self._process_list(data)

    def _process_list(self, data):
        data["results"] = [self.create_entity(**item) for item in data["results"]]
        return data

    def insert(self, entity: BaseEntity, user: User, **kwargs):
        uri, kwargs = self._get_uri(**kwargs)
        response = self.request.post(
            uri,
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data=entity.data,
            **kwargs,
        )
        return self.create_entity(**response.json())

    def update(self, entity: BaseEntity, user: User, **kwargs):
        uri, kwargs = self._get_uri(**kwargs)
        response = self.request.patch(
            f"{uri}{entity.id}/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data=entity.data,
            **kwargs,
        )
        return self.create_entity(**response.json())

    def save(self, entity: BaseEntity, user: User, **kwargs):
        if getattr(entity, "id", None):
            return self.update(entity, user, **kwargs)
        return self.insert(entity, user, **kwargs)

    def delete(self, entity: BaseEntity, user: User, **kwargs):
        uri, kwargs = self._get_uri(**kwargs)
        return self.request.delete(
            f"{uri}{entity.id}/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            **kwargs,
        )
