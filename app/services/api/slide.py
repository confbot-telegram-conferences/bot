from app.models.entities.user import User
from app.services.api.entities.slide import Slide
from app.services.api.entities.conference import Conference
from app.services.api.base_resource import BaseResource


class SlideApiService(BaseResource):
    def create_entity(self, **kwargs):
        return Slide(**kwargs)

    def get_uri(self, conference_id, **kwargs):
        return f"/api/conferences/{conference_id}/slides/", kwargs

    def set_as_viewed(self, user: User, conference: Conference, slide: Slide):
        url, _ = self.get_uri(conference_id=conference.id)
        return self.request.post(
            f"{url}{slide.id}/set_as_viewed/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={},
        )

    def send_image(self, user: User, chat_id, slide: Slide):
        url, _ = self.get_uri(conference_id=slide.conference)
        return self.request.post(
            f"{url}{slide.id}/send_image/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={"chat_id": chat_id},
        )

    def send_audio(self, user: User, chat_id, slide: Slide):
        url, _ = self.get_uri(conference_id=slide.conference)
        return self.request.post(
            f"{url}{slide.id}/send_audio/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={"chat_id": chat_id},
        )
