from app.services.api.entities.channel import Channel
from injector import inject
from app.services.api.channel import ChannelApiService
from app.bot_config.conversation_states_constants import CHANGE_NAME
from telegram import Update, InlineKeyboardButton, ParseMode, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from app.core.callback_context import CallbackContext
from app.transalation import trans as _


class NameConversation:
    @inject
    def __init__(self, channel_service: ChannelApiService):
        self.channel_service = channel_service

    def start(self, update: Update, context: CallbackContext) -> int:
        keyboard = [
            [
                InlineKeyboardButton(
                    text=_("back_in_history_btn"), callback_data="/myspace"
                ),
            ]
        ]
        update.effective_message.edit_text(
            _("channel_change_name"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return CHANGE_NAME

    def save_name(self, update: Update, context: CallbackContext):
        text = update.effective_message.text
        channel: Channel = self.channel_service.get(context.user)
        channel.name = text
        self.channel_service.update(channel, user=context.user)
        keyboard = [
            [
                InlineKeyboardButton(
                    text=_("start_my_space"), callback_data="/myspace"
                ),
            ]
        ]
        update.effective_message.reply_text(
            _("channel_change_name_done") % text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ConversationHandler.END
