from string import Template
from injector import inject
from app.services.api.entities.channel import Channel
from app.services.api.channel import ChannelApiService
from telegram import Update, InlineKeyboardButton, ParseMode, InlineKeyboardMarkup
from app.core.callback_context import CallbackContext
from app.handlers2.mixins.back_buttons_mixin import BackButtonsMixin
from app.transalation import trans as _


class ChannelManager(BackButtonsMixin):
    @inject
    def __init__(self, channel_service: ChannelApiService):
        self.channel_service = channel_service

    def callback(self, update: Update, context: CallbackContext):
        channel: Channel = self.channel_service.get(context.user)
        if channel.published:
            text = _("channel_published_button_desactive")
        else:
            text = _("channel_published_button_active")
        keyboard = [
            [
                InlineKeyboardButton(
                    text=_("channel_change_name_btn"),
                    callback_data="/channel_change_name",
                ),
                InlineKeyboardButton(text=text, callback_data="/channel_publish_start"),
            ],
            [
                InlineKeyboardButton(
                    text=_("start_command_myconferences"),
                    callback_data="/myconferences",
                ),
                InlineKeyboardButton(
                    text=_("start_command_conference_create"),
                    callback_data="/create_conference",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_("start_command_mycourses"), callback_data="/init_mycourses"
                ),
                InlineKeyboardButton(
                    text=_("start_command_course_create"),
                    callback_data="/create_course",
                ),
            ],
            self._get_back_buttons(command_back="/init_start_bot"),
        ]
        channel: Channel = self.channel_service.get(context.user)
        text = Template(_("my_space_command_hearder")).substitute(
            name=channel.name if channel.name else "-",
            published=_("Yes") if channel.published else _("No"),
        )
        update.effective_message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN,
        )
