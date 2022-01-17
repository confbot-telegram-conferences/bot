from app.services.api.entities.conference import Conference
from app.helpers import get_command_and_parameters
from typing import Any
from injector import Injector, inject
from app.core.translator import Translator
from app.mixins.paginage_mixin import PaginateMixin
from app.services.api.slide_admin import SlideAdminApiService
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context
from app.core.handler import Handler
from app.mixins.forward_mixin import ForwardMixin


class SlideListHandler(PaginateMixin, Handler, ForwardMixin):
    @inject
    def __init__(
        self,
        trans: Translator,
        injector: Injector,
        service: SlideAdminApiService,
        conference_service: ConferenceAdminApiService,
    ):
        super().__init__(trans=trans, injector=injector)
        self.service = service
        self.conference_service = conference_service

    def get_start_commands(self):
        return ["/slide_list"]

    def _load_parameters(self, context: Context):
        _, parameters = get_command_and_parameters(context.text)
        conference_id = parameters[0]
        conference: Conference = self.conference_service.get_by_id(
            conference_id, user=context.user
        )
        self._update_user_handler_data(
            context.user,
            {
                "conference_id": conference_id,
                "conference_name": conference.name,
            },
        )

    def _get_list_data(self, context: Context, **kwargs):
        service = self._get_service()
        conference_id = context.user.handler_data["conference_id"]
        data = service.list(
            user=context.user,
            conference_id=conference_id,
            **kwargs,
        )
        self._update_user_handler_data(context.user, {"count": data["count"]})
        return data

    def _get_service(self, **kwargs):
        return self.service

    def _get_item_command(self, item: Any, **kwargs):
        return f"/slide {str(item.id)}"

    def _get_create_command(self, context: Context, **kwargs):
        conference_id = context.user.handler_data["conference_id"]
        return f"/create_slide {conference_id}"

    def _get_list_header(self, context: Context, **kwargs):
        count = context.user.handler_data["count"]
        conference_name = context.user.handler_data["conference_name"]
        return self._("conference_create_slide_menu") % (conference_name, count)

    def _list_out(self, context: Context):
        conference_id = context.user.handler_data["conference_id"]
        return f"/conference {conference_id}"
