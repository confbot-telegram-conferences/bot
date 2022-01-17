from app.services.api.slide_admin import SlideAdminApiService
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context


class ChangeData:
    def _get_start_change(
        self,
        context: Context,
        conference_service: ConferenceAdminApiService,
        slide_service: SlideAdminApiService,
        step: str,
        ask_text: str,
    ):
        self._clear(context=context)
        context.user.step = step
        slide_id = context.user.handler_data["slide_id"]
        header = self._get_header(
            context=context,
            conference_service=conference_service,
            slide_service=slide_service,
        )
        buttons = [
            [
                context.create_button(
                    self._("back_in_history_btn"),
                    callback_data=f"/slide {slide_id}",
                )
            ]
        ]
        self._save_message_id(
            message=context.send_buttons(header + ask_text, buttons),
            context=context,
        )
