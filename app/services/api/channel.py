from app.services.api.base_resource import BaseResource
from app.services.api.entities.channel import Channel
from app.models.entities.user import User


class ChannelApiService(BaseResource):
    def create_entity(self, **kwargs):
        return Channel(**kwargs)

    def get_uri(self, **kwargs):
        return "/api/admin/channel"

    def get(self, user: User, **kwargs):
        uri, kwargs = self._get_uri(**kwargs)
        response = self.request.get(
            uri,
            headers=self.request.get_user_headers(user_id=user.backend_id),
            **kwargs,
        )
        return self.create_entity(**response.json())

    def update(self, entity: Channel, user: User, **kwargs):
        uri, kwargs = self._get_uri(**kwargs)
        response = self.request.patch(
            uri,
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data=entity.data,
            **kwargs,
        )
        return self.create_entity(**response.json())
