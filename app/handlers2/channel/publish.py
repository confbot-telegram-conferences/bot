from app.services.api.entities.channel import Channel
from app.services.api.channel import ChannelApiService
from app.core.callback_context import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from injector import inject
from app.transalation import trans as _


class PublishManager:
    @inject
    def __init__(self, channel_service: ChannelApiService):
        self.channel_service = channel_service

    def callback(self, update: Update, context: CallbackContext):
        back_button = InlineKeyboardButton(
            text=_("back_in_history_btn"), callback_data="/myspace"
        )
        channel: Channel = self.channel_service.get(context.user)
        if not channel.name:
            return update.effective_message.edit_text(
                text=_("channel_published_error_no_name"),
                reply_markup=InlineKeyboardMarkup([[back_button]]),
                parse_mode=ParseMode.MARKDOWN,
            )
        keyboard = [
            InlineKeyboardButton(
                text=_("Yes"),
                callback_data="/channel_publish_do_start",
            ),
            back_button,
        ]
        if channel.published:
            text = _("channel_published_stop")
        else:
            text = _("channel_published_start")
        update.effective_message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([keyboard]),
            parse_mode=ParseMode.MARKDOWN,
        )

    def activate_desactivate(self, update: Update, context: CallbackContext):
        keyboard = [
            InlineKeyboardButton(text=_("start_my_space"), callback_data="/myspace"),
        ]
        channel: Channel = self.channel_service.get(context.user)
        channel.published = not channel.published
        self.channel_service.update(channel, user=context.user)
        if channel.published:
            text = _("channel_published_start_done")
        else:
            text = _("channel_published_stop_done")
        update.effective_message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([keyboard]),
            parse_mode=ParseMode.MARKDOWN,
        )
