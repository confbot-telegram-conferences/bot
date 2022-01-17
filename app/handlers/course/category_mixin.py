from app.helpers import get_command_and_parameters
from app.services.api.entities.course import Course
from app.services.api.entities.category import Category
from app.services.api.category import CategoryApiService
from app.services.api.course_admin import CourseAdminApiService
from app.core.context import Context


class CategoryMixin:
    def command_change_category(
        self,
        context: Context,
        service: CourseAdminApiService,
        category_service: CategoryApiService,
    ):
        categories = category_service.list(user=context.user)
        buttons = []
        for i in range(0, len(categories), 3):
            current = []
            current.append(self._button_item(categories[i], context))
            if i + 1 < len(categories):
                current.append(self._button_item(categories[i + 1], context))
            if i + 2 < len(categories):
                current.append(self._button_item(categories[i + 2], context))
            buttons += [current]
        course_id = context.user.handler_data["course_id"]
        course: Course = service.get_by_id(course_id, user=context.user)
        buttons += [
            [
                context.create_button(
                    self._("back_in_history_btn"),
                    callback_data=f"/course {course_id}",
                ),
            ]
        ]
        header = self._get_header_text(course=course, context=context)
        return context.build_buttons(
            buttons, message=header + self._("course_create_change_category")
        )

    command_change_category.use_history = True

    def _button_item(self, item: Category, context: Context):
        return context.create_button(
            str(item), callback_data=f"/do_change_category {item.id}"
        )

    def command_do_change_category(
        self, context: Context, service: CourseAdminApiService
    ):
        course_id = context.user.handler_data["course_id"]
        course: Course = service.get_by_id(course_id, user=context.user)
        _, parameters = get_command_and_parameters(context.text)
        course.category = parameters[0]
        service.update(course, user=context.user)
        context.forward(f"/course {course_id}")

    command_do_change_category.use_history = True
