from app.mixins.back_buttons_mixin import BackButtonsMixin
from app.services.api.entities.category import Category
from app.services.api.category import CategoryApiService
from app.handlers.course.category_mixin import CategoryMixin
from app.handlers.course.remove_mixin import RemoveMixin
from app.handlers.course.name_mixin import NameMixin
from app.handlers.course.description_mixin import DescriptionMixin
from app.services.api.entities.course import Course
from app.services.api.course_admin import CourseAdminApiService
from string import Template
from app.config import Config
from app.helpers import get_command_and_parameters
from app.core.context import Context
from app.core.handler import Handler
from app.mixins.history_mixin import HistoryMixin


class CourseHandler(
    HistoryMixin,
    DescriptionMixin,
    NameMixin,
    RemoveMixin,
    CategoryMixin,
    BackButtonsMixin,
    Handler,
):
    def get_start_commands(self):
        return ["/course", "/init_course"]

    def start(
        self,
        context: Context,
        course_service: CourseAdminApiService,
        config: Config,
        category_service: CategoryApiService,
    ):
        command_start, parameters = get_command_and_parameters(context.text)
        context.user.current_handler = self.get_code()
        course: Course = course_service.get_by_id(parameters[0], user=context.user)
        category_name = ""
        if course.category:
            category: Category = category_service.get_by_id(
                course.category, user=context.user
            )
            category_name = category.name
        self._update_user_handler_data(
            context.user, {"course_id": course.id, "category_name": category_name}
        )
        share_link = config.get_shared_link(
            self._("course_wait_share_text") % course.name, course.share_id
        )
        buttons = [
            [
                context.create_button(
                    self._("course_wait_name_btn"), callback_data="/change_name"
                ),
                context.create_button(
                    self._("course_wait_description_btn"),
                    callback_data="/change_description",
                ),
            ],
            [
                context.create_button(
                    self._("course_wait_conferences"),
                    callback_data=f"/init_myconferences {course.id}",
                ),
                context.create_button(
                    self._("change_category"),
                    callback_data="/change_category",
                ),
            ],
            [
                context.create_button(self._("course_wait_share"), url=share_link),
            ],
            [
                context.create_button(
                    self._("course_remove"),
                    callback_data="/remove_course",
                )
            ],
            self._get_back_buttons(command_back="/mycourses", context=context),
        ]
        header = self._get_header_text(course=course, context=context)
        if command_start == "/course":
            return context.build_buttons(buttons, message=header)
        context.send_buttons(header, buttons)

    start.use_history = True

    def _get_header_text(self, course: Course, context: Context):
        category_name = context.user.handler_data["category_name"]
        return Template(self._("course_wait_principal_menu")).substitute(
            name=course.name,
            number_of_conferences=course.number_of_conferences,
            number_of_active_conferences=course.number_of_active_conferences,
            description=course.description,
            category=category_name,
        )
