from app.handlers.conference.active_mixin import ActiveMixin
from app.mixins.back_buttons_mixin import BackButtonsMixin
from app.handlers.conference.course_mixin import CourseMixin
from app.services.api.entities.course import Course
from app.services.api.course_admin import CourseAdminApiService
from app.core.translator import Translator
from injector import Injector, inject
from app.handlers.conference.remove_mixin import RemoveMixin
from string import Template
from app.config import Config
from app.services.api.conference_admin import ConferenceAdminApiService
from app.services.api.entities.conference import Conference
from app.helpers import get_command_and_parameters
from app.core.context import Context
from app.core.handler import Handler
from app.mixins.history_mixin import HistoryMixin
from app.handlers.conference.name_mixin import NameMixin
from app.handlers.conference.description_mixin import DescriptionMixin


class ConferenceHandler(
    HistoryMixin,
    DescriptionMixin,
    NameMixin,
    RemoveMixin,
    CourseMixin,
    ActiveMixin,
    BackButtonsMixin,
    Handler,
):
    @inject
    def __init__(
        self,
        trans: Translator,
        injector: Injector,
        course_service: CourseAdminApiService,
    ):
        super().__init__(trans=trans, injector=injector)
        self.course_service = course_service

    def get_start_commands(self):
        return ["/conference", "/init_conference", "/start_f_backend"]

    def start(
        self,
        context: Context,
        conference_service: ConferenceAdminApiService,
        config: Config,
    ):
        command_start, parameters = get_command_and_parameters(context.text)
        if command_start == "/start_f_backend":
            context.user.clear_context()
        context.user.current_handler = self.get_code()
        conference: Conference = conference_service.get_by_id(
            parameters[0], user=context.user
        )
        self._update_user_handler_data(context.user, {"conference_id": conference.id})
        share_link = config.get_shared_link(
            self._("conference_wait_share_text") % conference.name, conference.share_id
        )
        course_id = conference.course
        command_back = (
            f"/init_myconferences {course_id}" if course_id else "/myconferences"
        )
        active_desactive_lb = (
            self._("conference_desactive")
            if conference.active
            else self._("conference_active")
        )
        active_alerts_lb = (
            self._("conference_alert_desactive")
            if conference.alert_to_owner
            else self._("conference_alert_active")
        )
        conference_id = context.user.handler_data["conference_id"]
        buttons = [
            [
                context.create_button(
                    self._("conference_wait_name_btn"), callback_data="/change_name"
                ),
                context.create_button(
                    self._("conference_wait_description_btn"),
                    callback_data="/change_description",
                ),
            ],
            [
                context.create_button(
                    self._("conference_wait_slides"),
                    callback_data=f"/slide_list {conference.id}",
                ),
                context.create_button(
                    self._("conference_wait_show"),
                    callback_data=f"/show_conference {conference_id}",
                ),
            ],
            [
                context.create_button(
                    self._("conference_wait_open_in_group"),
                    switch_inline_query=conference.name,
                ),
                context.create_button(self._("conference_wait_share"), url=share_link),
            ],
            [
                context.create_button(
                    active_alerts_lb,
                    callback_data=f"/conference_alert_start {conference.id}",
                ),
                context.create_button(
                    active_desactive_lb, callback_data="/active_conference"
                ),
            ],
            [
                context.create_button(
                    self._("conference_change_category"),
                    callback_data="/change_course",
                ),
                context.create_button(
                    self._("conference_statistics"),
                    callback_data=f"/conference_statistics {conference.id}",
                ),
            ],
            [
                context.create_button(
                    self._("conference_upload_zip"),
                    callback_data=f"/update_by_zip {conference.id}",
                )
            ],
            [
                context.create_button(
                    self._("conference_remove"),
                    callback_data="/remove_conference",
                ),
            ],
            self._get_back_buttons(command_back=command_back, context=context),
        ]
        header = self._get_header_text(conference=conference, context=context)
        if command_start == "/conference":
            return context.build_buttons(buttons, message=header)
        context.send_buttons(header, buttons)

    start.use_history = True

    def _get_header_text(self, conference: Conference, context: Context):
        course = None
        if conference.course:
            course: Course = self.course_service.get_by_id(
                conference.course, user=context.user
            )
        return Template(self._("conference_wait_principal_menu")).substitute(
            name=conference.name,
            number_slides=conference.number_of_slides,
            description=conference.description,
            course=course.name if course else "-",
            active_desactive=self._("Yes") if conference.active else self._("No"),
            alert_active_desactive=self._("Yes")
            if conference.alert_to_owner
            else self._("No"),
        )
