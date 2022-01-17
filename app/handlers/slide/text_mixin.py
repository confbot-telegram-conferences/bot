from app.services.api.entities.slide import Slide
from app.services.api.slide_admin import SlideAdminApiService
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context


class TextMixin:
    def command_change_text(
        self,
        context: Context,
        conference_service: ConferenceAdminApiService,
        slide_service: SlideAdminApiService,
    ):
        return self._get_start_change(
            context=context,
            conference_service=conference_service,
            step="wait_change_text",
            ask_text=self._("command_change_text_get_name"),
            slide_service=slide_service,
        )

    def wait_change_text(self, context: Context, slide_service: SlideAdminApiService):
        slide_id = context.user.handler_data["slide_id"]
        conference_id = context.user.handler_data["conference_id"]
        if context.text:
            slide: Slide = slide_service.get_by_id(
                slide_id,
                conference_id=conference_id,
                user=context.user,
            )
            slide.text = context.text
            slide_service.update(slide, conference_id=conference_id, user=context.user)
        return context.forward(f"/init_slide {slide_id}")
