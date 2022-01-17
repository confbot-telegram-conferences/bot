from app.services.api.entities.conference import Conference
from app.services.api.conference_admin import ConferenceAdminApiService
from app.handlers2.mixins.back_buttons_mixin import BackButtonsMixin
from injector import inject
from app.helpers import get_command_and_parameters
from telegram import Update, InlineKeyboardMarkup, ParseMode, InlineKeyboardButton
from app.core.callback_context import CallbackContext
from app.transalation import trans as _


class AlertsManager(BackButtonsMixin):
    @inject
    def __init__(self, conference_service: ConferenceAdminApiService):
        self.conference_service = conference_service

    def callback(self, update: Update, context: CallbackContext):
        command, parameters = get_command_and_parameters(update.callback_query.data)
        conference_id = parameters[0]
        conference: Conference = self.conference_service.get_by_id(
            conference_id, context.user
        )
        keyboard = [
            InlineKeyboardButton(
                text=_("Yes"),
                callback_data=f"/conference_alert_do_start {conference_id}",
            ),
            InlineKeyboardButton(
                text=_("back_in_history_btn"),
                callback_data=f"/conference {conference_id}",
            ),
        ]
        conference = self.conference_service.get_by_id(conference_id, user=context.user)
        if conference.alert_to_owner:
            text = _("conference_alert_stop")
        else:
            text = _("conference_alert_start")
        update.effective_message.edit_text(
            text=text % conference.name,
            reply_markup=InlineKeyboardMarkup([keyboard]),
            parse_mode=ParseMode.MARKDOWN,
        )

    def activate_desactivate(self, update: Update, context: CallbackContext):
        command, parameters = get_command_and_parameters(update.callback_query.data)
        conference_id = parameters[0]
        keyboard = [
            InlineKeyboardButton(
                text=_("conference_wait_end_detail"),
                callback_data=f"/conference {conference_id}",
            ),
        ]
        conference = self.conference_service.get_by_id(conference_id, user=context.user)
        conference.alert_to_owner = not conference.alert_to_owner
        self.conference_service.save(conference, user=context.user)
        if conference.alert_to_owner:
            text = _("conference_alert_start_done")
        else:
            text = _("conference_alert_stop_done")
        update.effective_message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([keyboard]),
            parse_mode=ParseMode.MARKDOWN,
        )
