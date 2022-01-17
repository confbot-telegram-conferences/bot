from app.handlers2.mixins.show_slide_mixin import ShowSlideMixin
from blinker import signal
from app.helpers import reply_and_remove
from string import Template
from injector import inject
from telegram import Update
from telegram.error import BadRequest
from app.core.callback_context import CallbackContext
from app.services.api.slide import SlideApiService
from app.services.api.entities.conference import Conference
from app.services.api.conference import ConferenceApiService
from app.config import Config
from app.core.translator import Translator


class ShowInGroupManager(ShowSlideMixin):
    @inject
    def __init__(
        self,
        trans: Translator,
        conference_service: ConferenceApiService,
        config: Config,
        slide_service: SlideApiService,
    ):
        self.trans = trans
        self.conference_service = conference_service
        self.config = config
        self.slide_service = slide_service

    def start(self, update: Update, context: CallbackContext):
        conference_id = context.args[0] if len(context.args) > 0 else None
        if not conference_id:
            return update.message.reply_text(
                self.trans._("conference_group_show_not_id")
            )
        conference: Conference = self.conference_service.get_by_id(
            conference_id, user=context.user
        )
        if conference.number_of_slides == 0:
            return update.message.reply_text(
                self.trans._("conference_group_show_no_slides") % conference.name
            )
        context.user_data["conference_in_group"] = {
            "conference_id": conference_id,
            "step": 0,
        }
        text = Template(self.trans._("conference_group_show")).substitute(
            name=conference.name,
            number_slides=conference.number_of_slides,
            description=conference.description,
            bot_name=self.config.TELEGRAM_BOT_NAME,
        )
        update.message.reply_text(text)
        signal("start_conference_in_group").send(
            self,
            conference=conference,
            user=context.user,
            update=update,
        )

    def next(self, update: Update, context: CallbackContext):
        if not self._has_conference_active(context=context):
            return reply_and_remove(
                self.trans._("conference_group_show_next_error"), update=update
            )
        data = context.user_data["conference_in_group"]
        data["step"] = data["step"] + 1
        context.user_data["conference_in_group"] = data
        is_last = self._show_slide(update=update, context=context)
        if is_last:
            text = self._close_and_send_message(
                self.trans._("conference_group_show_end"), update, context
            )
            update.message.bot.send_message(text=text, chat_id=update.effective_chat.id)

    def _show_slide(self, update: Update, context: CallbackContext):
        data = context.user_data["conference_in_group"]
        conference_id = data["conference_id"]
        slide, is_last = self.conference_service.get_slide_by_position(
            user=context.user, conference_id=conference_id, index=data["step"]
        )
        self._send_slide_files(update=update, slide=slide, user=context.user)
        chat_id = update.effective_chat.id
        try:
            update.message.bot.delete_message(
                chat_id=chat_id, message_id=update.effective_message.message_id
            )
        except BadRequest:
            pass
        return is_last

    def close_conference(self, update: Update, context: CallbackContext):
        if not self._has_conference_active(context=context):
            return reply_and_remove(
                self.trans._("conference_group_show_close_error"), update=update
            )
        text = self._close_and_send_message(
            self.trans._("conference_group_was_closed"), update, context
        )
        update.message.reply_text(text)

    def _close_and_send_message(
        self, text_id, update: Update, context: CallbackContext
    ):
        conference_id = context.user_data["conference_in_group"]["conference_id"]
        context.user_data["conference_in_group"] = {}
        conference: Conference = self.conference_service.get_by_id(
            conference_id, user=context.user
        )
        link = self.config.get_shared_url(conference.share_id)
        return text_id % (conference.name, link)

    def _has_conference_active(self, context: CallbackContext):
        if "conference_in_group" not in context.user_data:
            return False
        conference_in_group = context.user_data["conference_in_group"]
        if "conference_id" not in conference_in_group:
            return False
        return True

    def show_same(self, update: Update, context: CallbackContext):
        if not self._has_conference_active(context=context):
            return reply_and_remove(
                self.trans._("conference_group_show_next_error"), update=update
            )
        data = context.user_data["conference_in_group"]
        if data["step"] == 0:
            return update.message.reply_text(
                self.trans._("conference_group_show_same_error")
            )
        self._show_slide(update=update, context=context)
