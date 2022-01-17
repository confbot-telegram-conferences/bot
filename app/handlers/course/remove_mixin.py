from app.services.api.entities.course import Course
from app.services.api.course_admin import CourseAdminApiService
from app.core.context import Context


class RemoveMixin:
    def command_remove_course(self, context: Context, service: CourseAdminApiService):
        course_id = context.user.handler_data["course_id"]
        course: Course = service.get_by_id(course_id, user=context.user)
        buttons = [
            [
                context.create_button(
                    self._("course_remove_btn"),
                    callback_data="/do_remove_course",
                ),
                self.create_back_button(context=context),
            ]
        ]
        header = self._get_header_text(course=course, context=context)
        return context.build_buttons(
            buttons,
            message=header + self._("course_remove_description_lb"),
        )

    command_remove_course.use_history = True

    def command_do_remove_course(
        self, context: Context, service: CourseAdminApiService
    ):
        course_id = context.user.handler_data["course_id"]
        course: Course = service.get_by_id(course_id, user=context.user)
        service.delete(course, user=context.user)
        context.forward("/mycourses")

    command_do_remove_course.use_history = True
