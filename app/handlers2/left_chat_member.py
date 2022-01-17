from app.services.api.group_channel_admin import GroupChannelAdminApiService
from app.config import Config
from telegram import Update
from app.core.callback_context import CallbackContext
from app.utils import inject_fuction
from app.core.exception import BackendException


@inject_fuction()
def left_chat_member(
    update: Update,
    context: CallbackContext,
    config: Config,
    group_channel_service: GroupChannelAdminApiService,
):
    if config.TELEGRAM_BOT_NAME != update.message.left_chat_member.username:
        return
    try:
        group_channel = group_channel_service.get_by_external_id(
            user=context.user, external_id=update.effective_chat.id
        )
        group_channel_service.desactive(user=context.user, group_channel=group_channel)
    except BackendException as e:
        if e.status_code != 404:
            raise e
