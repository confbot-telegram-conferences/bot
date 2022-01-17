from app.mixins.yes_no_buttons import YesNoButtonsMixin
from app.services.api.entities.course import Course
from app.services.api.course_admin import CourseAdminApiService
from app.core.context import Context
from app.core.handler import Handler
from app.mixins.forward_mixin import ForwardMixin
from app.helpers import is_no, is_yes


class CreateCourseHandler(ForwardMixin, YesNoButtonsMixin, Handler):
    def get_start_commands_with_description(self):
        return [("/create_course", self._("create_course_command_description"))]

    def get_start_commands(self):
        return ["/create_course"]

    def start(self, context: Context, **kwargs):
        context.user.current_handler = self.get_code()
        context.user.step = "wait_start"
        context.send_message(self._("course_start_text"))
        context.send_buttons(
            self._("course_start_question"), [self._yes_no_buttons(context=context)]
        )

    def wait_start(self, context: Context):
        if is_no(context.text):
            context.user.clear_context()
            context.send_buttons(
                self._("course_wait_start_clear"),
                [
                    [
                        context.create_button(
                            self._("go_to_start_btn"),
                            callback_data="/start",
                        )
                    ]
                ],
            )
            return
        if is_yes(context.text):
            context.user.step = "wait_name"
            return self._("course_wait_name")
        return self._("course_wait_start_yes_or_no")

    def wait_name(self, context: Context, service: CourseAdminApiService):
        course = service.insert(
            service.create_entity(name=context.text), user=context.user
        )
        self._update_user_handler_data(context.user, {"course_id": course.id})
        context.user.step = "wait_description"
        return self._("course_wait_description")

    def wait_description(self, context: Context, service: CourseAdminApiService):
        course_id = context.user.handler_data["course_id"]
        course: Course = service.get_by_id(course_id, user=context.user)
        course.description = context.text
        service.update(course, user=context.user)
        return context.forward(f"/init_course {course_id}")
