import emoji
from app.core.exception import BadBotRequestException
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, error
from app.core.context import Context
from .file import File

TELEGRAM_ID_FIELD = "telegram_id"


class TelegramContext(Context):
    def _send_message(self, text, **kwargs):
        return self.bot.send_message(
            chat_id=self.chat_id, text=self._prepare_text(text), **kwargs
        )

    def _update_message(self, text, message_id, **kwargs):
        try:
            return self.t_update.effective_message.edit_text(
                text=self._prepare_text(text), **kwargs
            )
        except error.BadRequest:
            raise BadBotRequestException()

    def _prepare_text(self, text):
        return emoji.emojize(text, use_aliases=True)

    def delete_message(self, message_id):
        return self.bot.delete_message(chat_id=self.chat_id, message_id=message_id)

    def _send_photo(self, photo):
        return self.bot.send_photo(chat_id=self.chat_id, photo=photo)

    def send_buttons(self, text, buttons, **kwargs):
        return self.send_message(**self.build_buttons(buttons, message=text), **kwargs)

    def build_buttons(self, buttons, **kwargs):
        return {**dict(reply_markup=InlineKeyboardMarkup(buttons)), **kwargs}

    def _send_voice(self, voice):
        return self.bot.send_voice(chat_id=self.chat_id, voice=voice)

    def get_text(self):
        return self.message.text

    def get_user(self):
        user = self.user_context
        data = {
            TELEGRAM_ID_FIELD: user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "language_code": user.language_code,
            "is_bot": user.is_bot,
        }
        return self.user_repository.get_or_create_user(
            user.id, {TELEGRAM_ID_FIELD: user.id}, data
        )

    def get_image(self):
        message = self.input["message"]
        photos = message.get("photo", [])
        data = None
        if len(photos) > 0:
            data = photos.pop()
        if not data:
            return
        return File(
            bot=self.bot,
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            ext="jpg",
        )

    def get_voice(self):
        if "voice" not in self.input["message"]:
            return None
        voice = self.input["message"]["voice"]
        return File(
            bot=self.bot,
            file_id=voice["file_id"],
            file_unique_id=voice["file_unique_id"],
            file_size=voice["file_size"],
            ext="ogg",
        )

    def get_audio(self):
        if "audio" not in self.input["message"]:
            return None
        audio = self.input["message"]["audio"]
        return File(
            bot=self.bot,
            file_id=audio["file_id"],
            file_unique_id=audio["file_unique_id"],
            file_size=audio["file_size"],
            file_name=audio["file_name"],
        )

    def get_document(self):
        if "document" not in self.input["message"]:
            return None
        document = self.input["message"]["document"]
        return File(bot=self.bot, **document)

    def create_button(self, text, **kwargs):
        return InlineKeyboardButton(text=self._prepare_text(text), **kwargs)
