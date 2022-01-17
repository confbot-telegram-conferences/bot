from app.services.api.entities.conference import Conference
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context


class RemoveMixin:
    def command_remove_conference(
        self, context: Context, service: ConferenceAdminApiService
    ):
        conference_id = context.user.handler_data["conference_id"]
        conference: Conference = service.get_by_id(conference_id, user=context.user)
        buttons = [
            [
                context.create_button(
                    self._("conference_remove_btn"),
                    callback_data="/do_remove_description",
                ),
                self.create_back_button(context=context),
            ]
        ]
        header = self._get_header_text(conference=conference, context=context)
        return context.build_buttons(
            buttons,
            message=header + self._("conference_remove_description_lb"),
        )

    command_remove_conference.use_history = True

    def command_do_remove_description(
        self, context: Context, service: ConferenceAdminApiService
    ):
        conference_id = context.user.handler_data["conference_id"]
        conference: Conference = service.get_by_id(conference_id, user=context.user)
        service.delete(conference, user=context.user)
        course_id = conference.course
        context.forward(
            f"/init_myconferences {course_id}" if course_id else "/myconferences"
        )

    command_do_remove_description.use_history = True
