from app.handlers2.mixins.back_buttons_mixin import BackButtonsMixin
from string import Template
from app.services.api.channel_plublic import ChannelPublicApiService
from injector import inject
from app.services.api.entities.channel import Channel
from app.helpers import get_command_and_parameters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from app.core.callback_context import CallbackContext
from app.transalation import trans as _


class ChannelDetailManager(BackButtonsMixin):
    @inject
    def __init__(self, service: ChannelPublicApiService):
        self.service = service

    def callback(self, update: Update, context: CallbackContext):
        keyboard = []
        key, params = get_command_and_parameters(update.callback_query.data)
        channel_id = params[0]
        channel: Channel = self.service.get_by_id(channel_id, user=context.user)
        context.user_data["channel_active"] = channel_id
        if channel.conference_count:
            keyboard += [
                [
                    InlineKeyboardButton(
                        text=_("channel_detail_conferences"),
                        callback_data=f"/channel_conferences {channel.id}",
                    ),
                ]
            ]
        if channel.course_count:
            keyboard += [
                [
                    InlineKeyboardButton(
                        text=_("channel_detail_courses"),
                        callback_data=f"/public_courses_channel {channel.id}",
                    ),
                ]
            ]
        keyboard += [self._get_back_buttons("/channel_public")]
        text = Template(_("channel_detail_header")).substitute(
            name=channel.name,
            course_count=channel.course_count,
            conference_count=channel.conference_count,
        )
        update.effective_message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN,
        )
