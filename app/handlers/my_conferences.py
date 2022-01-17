from string import Template
from app.services.api.entities.course import Course
from app.services.api.course_admin import CourseAdminApiService
from app.helpers import get_command_and_parameters
from app.core.context import Context
from app.core.handler import Handler
from typing import Any
from injector import Injector, inject
from app.core.translator import Translator
from app.mixins.paginage_mixin import PaginateMixin
from app.services.api.conference_admin import ConferenceAdminApiService


class MyConferencesHandler(PaginateMixin, Handler):
    @inject
    def __init__(
        self,
        trans: Translator,
        injector: Injector,
        service: ConferenceAdminApiService,
        course_service: CourseAdminApiService,
    ):
        super().__init__(trans=trans, injector=injector)
        self.service = service
        self.course_service = course_service

    def _load_parameters(self, context: Context, **kwargs):
        command, parameters = get_command_and_parameters(context.text)
        if command == "/init_myconferences":
            self._update_user_handler_data(context.user, {"course_id": parameters[0]})
        else:
            self._update_user_handler_data(context.user, {"course_id": None})

    def _get_list_data(self, context: Context, **kwargs):
        service = self._get_service()
        course_id = context.user.handler_data["course_id"]
        params = {}
        if course_id:
            params["course"] = course_id
        else:
            params["orphan_conferences"] = True
        data = service.list(user=context.user, **params, **kwargs)
        self._update_user_handler_data(context.user, {"count": data["count"]})
        return data

    def get_start_commands(self):
        return ["/myconferences", "/init_myconferences"]

    def _get_service(self, **kwargs):
        return self.service

    def _get_item_command(self, item: Any, **kwargs):
        return f"/conference {str(item.id)}"

    def _get_create_command(self, context: Context, **kwargs):
        course_id = context.user.handler_data["course_id"]
        if course_id:
            return f"/create_conference {course_id}"
        return "/create_conference"

    def _get_list_header(self, context: Context, **kwargs):
        count = context.user.handler_data["count"]
        course_id = context.user.handler_data["course_id"]
        if course_id:
            course: Course = self.course_service.get_by_id(course_id, user=context.user)
            return Template(self._("conference_admin_list_menu_course")).substitute(
                name=course.name,
                number_of_conferences=course.number_of_conferences,
                description=course.description,
            )
        return self._("conference_admin_list_menu") % count

    def _list_out(self, context: Context, **kwargs):
        course_id = context.user.handler_data["course_id"]
        if course_id:
            return f"/course {course_id}"
        return "/myspace"
