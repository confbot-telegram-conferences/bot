from app.services.api.course_admin import CourseAdminApiService
from app.core.context import Context
from app.core.handler import Handler
from typing import Any
from injector import Injector, inject
from app.core.translator import Translator
from app.mixins.paginage_mixin import PaginateMixin


class MyCoursesHandler(PaginateMixin, Handler):
    @inject
    def __init__(
        self, trans: Translator, injector: Injector, service: CourseAdminApiService
    ):
        super().__init__(trans=trans, injector=injector)
        self.service = service

    def _get_list_data(self, context: Context, **kwargs):
        service = self._get_service()
        data = service.list(user=context.user, **kwargs)
        self._update_user_handler_data(context.user, {"count": data["count"]})
        return data

    def get_start_commands_with_description(self):
        return [("/mycourses", self._("mycourses_command_description"))]

    def get_start_commands(self):
        return ["/mycourses", "/init_mycourses"]

    def _get_service(self, **kwargs):
        return self.service

    def _get_item_command(self, item: Any, **kwargs):
        return f"/course {str(item.id)}"

    def _get_create_command(self, **kwargs):
        return "/create_course"

    def _get_list_header(self, context: Context, **kwargs):
        count = context.user.handler_data["count"]
        return self._("course_admin_list_menu") % count

    def _list_out(self, context: Context, **kwargs):
        return "/myspace"
