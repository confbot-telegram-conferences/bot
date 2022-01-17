from app.services.api.entities.slide import Slide
from app.services.api.slide_admin import SlideAdminApiService
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context


class RemoveMixin:
    def command_slide_remove(
        self,
        context: Context,
        service: ConferenceAdminApiService,
        slide_service: SlideAdminApiService,
    ):
        self._clear(context=context)
        slide_id = context.user.handler_data["slide_id"]
        buttons = [
            [
                context.create_button(
                    self._("slide_remove_btn"),
                    callback_data="/do_remove_slide",
                ),
                context.create_button(
                    self._("back_in_history_btn"),
                    callback_data=f"/slide {slide_id}",
                ),
            ]
        ]
        header = self._get_header(
            conference_service=service, context=context, slide_service=slide_service
        )
        return context.build_buttons(
            buttons,
            message=header + self._("slide_remove_ask"),
        )

    def command_do_remove_slide(self, context: Context, service: SlideAdminApiService):
        conference_id = context.user.handler_data["conference_id"]
        slide_id = context.user.handler_data["slide_id"]
        slide: Slide = service.get_by_id(
            slide_id, conference_id=conference_id, user=context.user
        )
        service.delete(slide, conference_id=conference_id, user=context.user)
        return context.forward(f"/slide_list {conference_id}")
