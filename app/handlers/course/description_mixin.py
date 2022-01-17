from app.services.api.entities.course import Course
from app.services.api.course_admin import CourseAdminApiService
from app.core.context import Context


class DescriptionMixin:
    def command_change_description(
        self, context: Context, service: CourseAdminApiService
    ):
        context.user.step = "wait_change_description"
        course_id = context.user.handler_data["course_id"]
        course: Course = service.get_by_id(course_id, user=context.user)
        buttons = [
            [
                self.create_back_button(context=context),
            ]
        ]
        header = self._get_header_text(course=course, context=context)
        return context.build_buttons(
            buttons, message=header + self._("course_create_change_description")
        )

    command_change_description.use_history = True

    def wait_change_description(self, context: Context, service: CourseAdminApiService):
        course_id = context.user.handler_data["course_id"]
        if context.text:
            course: Course = service.get_by_id(course_id, user=context.user)
            course.description = context.text
            service.update(course, user=context.user)
        return context.forward(f"/init_course {course_id}")

    wait_change_description.clear_history = True
