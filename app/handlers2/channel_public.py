from typing import Any
from injector import inject
from app.services.api.channel_plublic import ChannelPublicApiService
from app.handlers2.mixins.paginage_mixin import PaginateMixin
from telegram import Update
from app.core.callback_context import CallbackContext
from app.transalation import trans as _


class ChannelPublicManager(PaginateMixin):
    @inject
    def __init__(self, service: ChannelPublicApiService):
        self.service = service

    def _get_service(self, **kwargs):
        return self.service

    def _get_item_command(self, item: Any, **kwargs):
        return f"/channel_detail {str(item.id)}"

    def _get_list_header(self, data, **kwargs):
        return (
            _("channel_public_header")
            if len(data["results"]) > 0
            else _("channel_public_header_empty")
        )

    def _callback_subfix(self, **kwargs):
        return "channel_public"

    def _extra_buttons(self, update: Update, context: CallbackContext):
        command_back = self._list_out(context=context)
        return [self._get_back_buttons(command_back=command_back)]

    def callback(self, update: Update, context: CallbackContext):
        update.effective_message.edit_text(**self.paginate(update, context))
