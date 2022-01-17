from app.services.api.entities.conference import Conference
from app.services.api.conference_admin import ConferenceAdminApiService
from app.helpers import get_command_and_parameters
from app.services.api.course_admin import CourseAdminApiService
from app.core.context import Context


class CourseMixin:
    def command_change_course(
        self,
        context: Context,
        service: ConferenceAdminApiService,
        course_service: CourseAdminApiService,
    ):
        courses = course_service.list(
            user=context.user,
            params={"page": 1, "page_size": 100},
        )
        buttons = []
        conference_id = context.user.handler_data["conference_id"]
        conference: Conference = service.get_by_id(conference_id, user=context.user)
        course_id = conference.course
        for item in filter(lambda item: item.id != course_id, courses["results"]):
            buttons += [[self._button_item(item, context)]]
        buttons += [
            [
                context.create_button(
                    self._("back_in_history_btn"),
                    callback_data=f"/conference {conference_id}",
                ),
            ]
        ]
        header = self._get_header_text(conference=conference, context=context)
        return context.build_buttons(
            buttons, message=header + self._("conference_create_change_course")
        )

    command_change_course.use_history = True

    def _button_item(self, item: Conference, context: Context):
        return context.create_button(
            str(item), callback_data=f"/do_change_course {item.id}"
        )

    def command_do_change_course(
        self, context: Context, service: ConferenceAdminApiService
    ):
        conference_id = context.user.handler_data["conference_id"]
        conference: Conference = service.get_by_id(conference_id, user=context.user)
        _, parameters = get_command_and_parameters(context.text)
        conference.course = parameters[0]
        service.update(conference, user=context.user)
        context.forward(f"/conference {conference_id}")

    command_do_change_course.use_history = True
