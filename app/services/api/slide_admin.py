from app.models.entities.user import User
from app.services.api.slide import SlideApiService
from app.services.api.entities.slide import Slide


class SlideAdminApiService(SlideApiService):
    def create_entity(self, **kwargs):
        return Slide(**kwargs)

    def get_uri(self, conference_id, **kwargs):
        return (f"/api/admin/conferences/{conference_id}/slides/", kwargs)

    def upload_image(self, file_data, user: User, slide: Slide):
        url, _ = self.get_uri(conference_id=slide.conference)
        return self.request.post(
            f"{url}{slide.id}/save_image/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data=file_data,
        )

    def upload_audio(self, file_data, user: User, slide: Slide):
        url, _ = self.get_uri(conference_id=slide.conference)
        return self.request.post(
            f"{url}{slide.id}/save_audio/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data=file_data,
        )
