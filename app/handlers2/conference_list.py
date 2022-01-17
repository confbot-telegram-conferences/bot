from app.services.api.conference import ConferenceApiService
from app.services.api.entities.channel import Channel
from app.helpers import get_command_and_parameters
from typing import Any
from injector import inject
from app.services.api.channel_plublic import ChannelPublicApiService
from app.handlers2.mixins.paginage_mixin import PaginateMixin
from telegram import Update
from app.core.callback_context import CallbackContext
from app.transalation import trans as _


class ConferenceListManager(PaginateMixin):
    @inject
    def __init__(
        self, service: ConferenceApiService, channel_service: ChannelPublicApiService
    ):
        self.service = service
        self.channel_service = channel_service

    def _get_service(self, **kwargs):
        return self.service

    def _get_item_command(self, item: Any, **kwargs):
        return f"/show_conference {str(item.id)}"

    def _get_list_header(self, context: CallbackContext, **kwargs):
        channel: Channel = self.channel_service.get_by_id(
            context.user_data["channel_active"], context.user
        )
        return _("channel_conferences_header") % channel.name

    def _callback_subfix(self, **kwargs):
        return "channel_conferences"

    def _extra_buttons(self, update: Update, context: CallbackContext):
        command_back = self._list_out(context=context)
        return [self._get_back_buttons(command_back=command_back)]

    def callback(self, update: Update, context: CallbackContext):
        key, params = get_command_and_parameters(update.callback_query.data)
        context.user_data["conference_channel"] = {"channel_id": params[0]}
        update.effective_message.edit_text(**self.paginate(update, context))

    def _get_list_data(self, update: Update, context: CallbackContext, **kwargs):
        service = self._get_service()
        user_data = context.user_data["conference_channel"]
        params = {"channel": user_data["channel_id"]}
        data = service.list(
            user=context.user, orphan_conferences=True, **params, **kwargs
        )
        context.user_data["conference_channel"] = {
            **user_data,
            **{"count": data["count"]},
        }
        return data

    def _list_out(self, context: CallbackContext, **kwargs):
        return f'/channel_detail {context.user_data["channel_active"]}'
