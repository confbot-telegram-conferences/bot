from app.core.exception import BackendException
from app.mixins.forward_mixin import ForwardMixin
from app.telegram.file import File
from app.services.api.entities.slide import Slide
from app.services.api.slide_admin import SlideAdminApiService
from app.core.context import Context
from app.core.handler import Handler
from app.mixins.voice_audio_mixin import VoiceAudioMixin
from app.helpers import get_command_and_parameters


class CreateSlideHandler(ForwardMixin, VoiceAudioMixin, Handler):
    def get_start_commands(self):
        return ["/create_slide"]

    def start(self, context: Context, **kwargs):
        _, parameters = get_command_and_parameters(context.text)
        context.user.step = "wait_text"
        context.user.current_handler = self.get_code()
        conference_id = parameters[0]
        self._update_user_handler_data(context.user, {"conference_id": conference_id})
        buttons = [
            [
                context.create_button(
                    self._("back_in_history_btn"),
                    callback_data=f"/slide_list {conference_id}",
                )
            ]
        ]
        return context.build_buttons(
            buttons, message=self._("conference_wait_slide_text")
        )

    start.use_history = True

    def wait_text(self, context: Context, slide_service: SlideAdminApiService):
        slide = Slide()
        slide.text = context.text
        conference_id = context.user.handler_data["conference_id"]
        slide = slide_service.save(
            slide, user=context.user, conference_id=conference_id
        )
        context.user.step = "wait_slide"
        self._update_user_handler_data(context.user, {"slide_id": slide.id})
        return self._("create_slide_image")

    def wait_slide(self, context: Context, slide_service: SlideAdminApiService):
        conference_id = context.user.handler_data["conference_id"]
        slide: Slide = slide_service.get_by_id(
            context.user.handler_data["slide_id"],
            user=context.user,
            conference_id=conference_id,
        )
        image: File = context.get_image()
        if image:
            slide_service.upload_image(image.get_data(), user=context.user, slide=slide)
            context.user.step = "wait_voice"
            return self._("conference_wait_slide_voice")
        else:
            return self._("conference_wait_slide_image_error")

    def wait_voice(self, context: Context, slide_service: SlideAdminApiService):
        try:
            file: File = self.get_voice_audio(context=context)
            conference_id = context.user.handler_data["conference_id"]
            slide: Slide = slide_service.get_by_id(
                context.user.handler_data["slide_id"],
                user=context.user,
                conference_id=conference_id,
            )
            if file:
                slide_service.upload_audio(
                    file.get_data(), user=context.user, slide=slide
                )
            return context.forward(f"/init_slide {slide.id}")
        except BackendException as e:
            context.send_message(
                self._("error_max_size_file") % e.response_data["max_size"]
            )
