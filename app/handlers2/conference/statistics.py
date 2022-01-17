from app.services.api.conference import ConferenceApiService
from string import Template
from app.handlers2.mixins.back_buttons_mixin import BackButtonsMixin
from injector import inject
from app.helpers import get_command_and_parameters
from telegram import Update, InlineKeyboardMarkup, ParseMode
from app.core.callback_context import CallbackContext
from app.transalation import trans as _


class StatisticsManager(BackButtonsMixin):
    @inject
    def __init__(self, conference_service: ConferenceApiService):
        self.conference_service = conference_service

    def callback(self, update: Update, context: CallbackContext):
        command, parameters = get_command_and_parameters(update.callback_query.data)
        conference_id = parameters[0]
        data = self.conference_service.statistics(conference_id, context.user).json()
        keyboard = self._get_back_buttons(command_back=f"/conference {conference_id}")
        conference = self.conference_service.get_by_id(conference_id, user=context.user)
        text = Template(_("conference_statistics_text")).substitute(
            name=conference.name,
            count_unique_show=data["count_unique_show"],
            evaluation_avg=data["evaluation_avg"],
            slide_show_avg=data["slide_show_avg"],
            count_slide=data["count_slide"],
        )
        update.effective_message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([keyboard]),
            parse_mode=ParseMode.MARKDOWN,
        )
