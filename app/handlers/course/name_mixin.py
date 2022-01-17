from app.services.api.entities.course import Course
from app.services.api.course_admin import CourseAdminApiService
from app.core.context import Context


class NameMixin:
    def command_change_name(self, context: Context, service: CourseAdminApiService):
        context.user.step = "wait_change_name"
        buttons = [
            [
                self.create_back_button(context=context),
            ]
        ]
        course_id = context.user.handler_data["course_id"]
        course: Course = service.get_by_id(course_id, user=context.user)
        header = self._get_header_text(course=course, context=context)
        return context.build_buttons(
            buttons, message=header + self._("course_create_change_name")
        )

    command_change_name.use_history = True

    def wait_change_name(self, context: Context, service: CourseAdminApiService):
        course_id = context.user.handler_data["course_id"]
        if context.text:
            course: Course = service.get_by_id(course_id, user=context.user)
            course.name = context.text
            service.update(course, user=context.user)
        return context.forward(f"/init_course {course_id}")

    wait_change_name.clear_history = True
