from app.mixins.voice_audio_mixin import VoiceAudioMixin
from app.handlers.slide.remove_mixin import RemoveMixin
from app.handlers.slide.voice_mixin import VoiceMixin
from app.handlers.slide.change_data import ChangeData
from app.handlers.slide.image_mixin import ImageMixin
from app.handlers.slide.text_mixin import TextMixin
from app.services.api.entities.conference import Conference
from app.services.api.conference_admin import ConferenceAdminApiService
from app.services.api.slide_admin import SlideAdminApiService
from app.services.api.entities.slide import Slide
from app.helpers import get_command_and_parameters
from app.core.context import Context
from app.core.handler import Handler


class SideHandler(
    TextMixin, ImageMixin, VoiceMixin, RemoveMixin, ChangeData, VoiceAudioMixin, Handler
):
    def get_start_commands(self):
        return ["/slide", "/init_slide"]

    def start(
        self,
        context: Context,
        slide_service: SlideAdminApiService,
        conference_service: ConferenceAdminApiService,
    ):
        command, parameters = get_command_and_parameters(context.text)
        if command == "/slide":
            context.delete_last_message()
        self._update_user_handler_data(context.user, {"slide_messages": []})
        context.user.current_handler = self.get_code()
        conference_id = context.user.handler_data["conference_id"]
        slide_id = parameters[0]
        self._update_user_handler_data(context.user, {"slide_id": slide_id})
        slide: Slide = slide_service.get_by_id(
            slide_id,
            conference_id=conference_id,
            user=context.user,
        )
        self._save_message_id(
            message=context.send_message(
                self._get_header(
                    context=context,
                    conference_service=conference_service,
                    slide_service=slide_service,
                )
            ),
            context=context,
        )
        if slide.image_id:
            photo_message = slide_service.send_image(
                user=context.user, chat_id=context.chat_id, slide=slide
            )
            self._save_message_id(message=photo_message.json(), context=context)
        if slide.voice_id:
            audio_message = slide_service.send_audio(
                user=context.user, chat_id=context.chat_id, slide=slide
            )
            self._save_message_id(message=audio_message.json(), context=context)
        buttons = [
            [
                context.create_button(
                    self._("slide_command_change_text"),
                    callback_data="/change_text",
                ),
                context.create_button(
                    self._("slide_command_change_image"),
                    callback_data="/change_image",
                ),
                context.create_button(
                    self._("slide_command_change_voice"),
                    callback_data="/change_voice",
                ),
            ],
            [
                context.create_button(
                    self._("slide_remove"),
                    callback_data="/slide_remove",
                ),
            ],
            [
                context.create_button(
                    self._("back_in_history_btn"),
                    callback_data="/back",
                )
            ],
        ]
        text = f"{slide.position}: {slide.text}"
        self._save_message_id(
            message=context.send_buttons(text, buttons), context=context
        )

    def _save_message_id(self, message, context: Context):
        slide_messages = context.user.handler_data.get("slide_messages", [])
        slide_messages += [message["message_id"]]
        self._update_user_handler_data(context.user, {"slide_messages": slide_messages})

    def _get_header(
        self,
        context: Context,
        conference_service: ConferenceAdminApiService,
        slide_service: SlideAdminApiService,
    ):
        conference_id = context.user.handler_data["conference_id"]
        slide_id = context.user.handler_data["slide_id"]
        conference_id = context.user.handler_data["conference_id"]
        slide: Slide = slide_service.get_by_id(
            slide_id,
            conference_id=conference_id,
            user=context.user,
        )
        conference: Conference = conference_service.get_by_id(
            conference_id, user=context.user
        )
        return self._("slide_header") % (slide.position, conference.name)

    def _clear(self, context: Context):
        slide_messages = context.user.handler_data["slide_messages"]
        for message_id in slide_messages:
            context.delete_message(message_id=message_id)
        self._update_user_handler_data(context.user, {"slide_messages": []})

    def command_back(self, context: Context):
        self._clear(context=context)
        conference_id = context.user.handler_data["conference_id"]
        return context.forward(f"/slide_list {conference_id}")
