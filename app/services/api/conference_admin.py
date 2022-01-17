from app.models.entities.user import User
from app.services.api.entities.conference import Conference
from app.services.api.base_resource import BaseResource


class ConferenceAdminApiService(BaseResource):
    def create_entity(self, **kwargs):
        return Conference(**kwargs)

    def get_uri(self, course=None, orphan_conferences=None, params=None, **kwargs):
        params = params if params else {}
        if course:
            params["course"] = course
        if orphan_conferences:
            params["orphan_conferences"] = orphan_conferences
        return "/api/admin/conferences/", {**kwargs, **{"params": params}}

    def _save_file(
        self,
        file_data,
        user: User,
        conference: Conference,
        type,
        slide_position,
        method,
    ):
        url, _ = self.get_uri()
        conference_id = conference.id
        return self.request.post(
            f"{url}{conference_id}/{method}/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={
                "file_data": file_data,
                "type": type,
                "slide_position": slide_position,
            },
        )

    def save_image(
        self, file_data, user: User, conference: Conference, type, slide_position
    ):
        return self._save_file(
            file_data, user, conference, type, slide_position, "save_image"
        )

    def save_audio(
        self, file_data, user: User, conference: Conference, type, slide_position
    ):
        return self._save_file(
            file_data, user, conference, type, slide_position, "save_audio"
        )

    def clear_slides(self, user: User, conference: Conference):
        conference_id = (
            conference.id if isinstance(conference, Conference) else conference
        )
        url, _ = self.get_uri()
        return self.request.post(
            f"{url}{conference_id}/clear_slides/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={},
        )

    def upload_zip_file(self, file_data, user: User, conference: Conference = None):
        url, _ = self.get_uri()
        conference_id = (
            conference.id if isinstance(conference, Conference) else conference
        )
        return self.request.post(
            f"{url}upload_zip_file/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={"file_data": file_data, "conference_id": conference_id},
        )

    def download_zip_file(self, user: User, conference_id, chat_id):
        url, _ = self.get_uri()
        return self.request.post(
            f"{url}{conference_id}/download_zip_file/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={"chat_id": chat_id},
        )
