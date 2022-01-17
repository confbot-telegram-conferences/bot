import emoji
from app.models.repositories.user_repository import UserRepository
from app.handlers2.conference.upload_zip_mixin import UploadZipMixin
from app.helpers import get_command_and_parameters
from injector import inject
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.update import Update
from app.config import Config
from app.services.api.conference_admin import ConferenceAdminApiService
from app.transalation import trans as _
from app.bot_config import conversation_states_constants as constants


class UpdateByZipManager(UploadZipMixin):
    @inject
    def __init__(
        self,
        conference_service: ConferenceAdminApiService,
        user_repository: UserRepository,
        config: Config,
    ):
        self.conference_service = conference_service
        self.config = config
        self.ZIP = constants.CONFERENCE_UPDATE_ZIP
        self.user_repository = user_repository

    def start(self, update: Update, context: CallbackContext) -> int:
        command, parameters = get_command_and_parameters(update.callback_query.data)
        conference_id = parameters[0]
        context.user_data["create_or_update_conference"] = {
            "conference_id": conference_id
        }
        keyboard = [
            [
                InlineKeyboardButton(
                    _("conference_wait_ask_name_btn"),
                    callback_data="/start_upload_update_by_zip",
                ),
                InlineKeyboardButton(
                    _("conference_wait_give_zipe_btn"),
                    callback_data="/give_zip_update_by_zip",
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.effective_message.edit_text(
            emoji.emojize(_("update_by_zip_start_text"), use_aliases=True),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

    def start_upload(self, update: Update, context: CallbackContext) -> int:
        keyboard = [
            [
                InlineKeyboardButton(
                    _("update_by_zip_clear_files_btn"),
                    callback_data="/clear_slides_update_by_zip",
                ),
            ],
            [
                InlineKeyboardButton(
                    _("update_by_zip_upload_btn"),
                    callback_data="/upload_files_start_update_by_zip",
                ),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.effective_message.edit_text(
            emoji.emojize(_("update_by_zip_text"), use_aliases=True),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

    def start_zip(self, update: Update, context: CallbackContext) -> int:
        update.effective_message.edit_text(_("conference_wait_zip"))
        return constants.CONFERENCE_UPDATE_ZIP

    def clear_slides(self, update: Update, context: CallbackContext) -> int:
        conference_id = context.user_data["create_or_update_conference"][
            "conference_id"
        ]
        self.conference_service.clear_slides(
            user=update.model_user, conference=conference_id
        )
        text_1 = _("update_by_zip_slides_removed")
        text_2 = _("conference_wait_zip")
        text = f"{text_1}\n\n{text_2}"
        update.effective_message.edit_text(text)
        return constants.CONFERENCE_UPDATE_ZIP
