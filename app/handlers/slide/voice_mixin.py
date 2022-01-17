from app.core.file import File
from app.core.exception import BackendException
from app.services.api.entities.slide import Slide
from app.services.api.slide_admin import SlideAdminApiService
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context


class VoiceMixin:
    def command_change_voice(
        self,
        context: Context,
        conference_service: ConferenceAdminApiService,
        slide_service: SlideAdminApiService,
    ):
        return self._get_start_change(
            context=context,
            conference_service=conference_service,
            step="wait_change_voice",
            ask_text=self._("command_change_text_get_voice"),
            slide_service=slide_service,
        )

    def wait_change_voice(self, context: Context, slide_service: SlideAdminApiService):
        try:
            file: File = self.get_voice_audio(context=context)
            slide_id = context.user.handler_data["slide_id"]
            if file:
                conference_id = context.user.handler_data["conference_id"]
                slide: Slide = slide_service.get_by_id(
                    slide_id,
                    conference_id=conference_id,
                    user=context.user,
                )
                slide_service.upload_audio(
                    file.get_data(), user=context.user, slide=slide
                )
                return context.forward(f"/init_slide {slide_id}")
        except BackendException as e:
            context.send_message(
                self._("error_max_size_file") % e.response_data["max_size"]
            )
