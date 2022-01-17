import emoji
from app.models.repositories.user_repository import UserRepository
from app.handlers2.conference.upload_zip_mixin import UploadZipMixin
from app.config import Config
from app.helpers import get_command_and_parameters
from app.services.api.conference_admin import ConferenceAdminApiService
from injector import inject
from telegram.ext import CallbackContext
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update
from app.transalation import trans as _
from app.bot_config import conversation_states_constants as constants


class ConferenceCreateManager(UploadZipMixin):
    @inject
    def __init__(
        self,
        conference_service: ConferenceAdminApiService,
        user_repository: UserRepository,
        config: Config,
    ):
        self.conference_service = conference_service
        self.config = config
        self.ZIP = constants.CONFERENCE_CREATE_ZIP
        self.user_repository = user_repository

    def start(self, update: Update, context: CallbackContext) -> int:
        course_id = None
        if update.callback_query:
            command, parameters = get_command_and_parameters(update.callback_query.data)
            course_id = parameters[0] if len(parameters) else None
        context.user_data["create_or_update_conference"] = {"course_id": course_id}
        keyboard = [
            [
                InlineKeyboardButton(
                    _("conference_wait_ask_name_btn"),
                    callback_data="/ask_name_create_conference",
                ),
                InlineKeyboardButton(
                    _("conference_wait_give_zipe_btn"),
                    callback_data="/give_zip_create_conference",
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.effective_message.edit_text(
            emoji.emojize(_("conference_start_text"), use_aliases=True),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

    def ask_name(self, update: Update, context: CallbackContext):
        update.effective_message.reply_text(_("conference_wait_name"))
        return constants.CONFERENCE_CREATE_NAME

    def save_name(self, update: Update, context: CallbackContext):
        text = update.message.text
        data = context.user_data["create_or_update_conference"]
        context.user_data["create_or_update_conference"] = {**data, **{"name": text}}
        update.message.reply_text(_("conference_wait_description"))
        return constants.CONFERENCE_CREATE_DESCRIPTION

    def save_description(self, update: Update, context: CallbackContext):
        text = update.message.text
        data = context.user_data["create_or_update_conference"]
        entity = self.conference_service.create_entity(
            name=data["name"], description=text, course=data["course_id"]
        )
        entity = self.conference_service.save(entity, user=update.model_user)
        context.user_data["create_or_update_conference"] = {"conference_id": entity.id}
        update.message.reply_text(_("conference_wait_zip"))
        return constants.CONFERENCE_CREATE_ZIP
