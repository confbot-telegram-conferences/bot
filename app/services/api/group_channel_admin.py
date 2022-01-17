from app.services.api.entities.conference import Conference
from app.models.entities.user import User
from app.services.api.entities.group_channel import GroupChannel
from app.services.api.base_resource import BaseResource


class GroupChannelAdminApiService(BaseResource):
    def create_entity(self, **kwargs):
        return GroupChannel(**kwargs)

    def get_uri(self, **kwargs):
        return "/api/admin/group-channels/", kwargs

    def start_conference(
        self, user: User, conference: Conference, group_channel: GroupChannel
    ):
        url, _ = self.get_uri()
        return self.request.post(
            f"{url}{group_channel.id}/start_conference/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={"conference_id": conference.id},
        )

    def desactive(self, user: User, group_channel: GroupChannel):
        url, _ = self.get_uri()
        return self.request.post(
            f"{url}{group_channel.id}/desactive/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={},
        )

    def get_by_external_id(self, user: User, external_id):
        url, _ = self.get_uri()
        response = self.request.get(
            f"{url}get_by_external_id/{external_id}/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
        )
        return self.create_entity(**response.json())
