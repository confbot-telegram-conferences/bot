from app.services.api.entities.channel import Channel
from app.services.api.base_resource import BaseResource


class ChannelPublicApiService(BaseResource):
    def create_entity(self, **kwargs):
        return Channel(**kwargs)

    def get_uri(self, **kwargs):
        return "/api/channels/"
