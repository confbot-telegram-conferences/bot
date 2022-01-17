from app.telegram.file import File
from app.services.api.entities.slide import Slide
from app.services.api.slide_admin import SlideAdminApiService
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context


class ImageMixin:
    def command_change_image(
        self,
        context: Context,
        conference_service: ConferenceAdminApiService,
        slide_service: SlideAdminApiService,
    ):
        return self._get_start_change(
            context=context,
            conference_service=conference_service,
            slide_service=slide_service,
            step="wait_change_image",
            ask_text=self._("command_change_text_get_image"),
        )

    def wait_change_image(self, context: Context, slide_service: SlideAdminApiService):
        image: File = context.get_image()
        slide_id = context.user.handler_data["slide_id"]
        if image:
            conference_id = context.user.handler_data["conference_id"]
            slide: Slide = slide_service.get_by_id(
                slide_id,
                conference_id=conference_id,
                user=context.user,
            )
            slide_service.upload_image(image.get_data(), user=context.user, slide=slide)
        return context.forward(f"/init_slide {slide_id}")
