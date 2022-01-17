import gettext
import time
from telegram.error import BadRequest
from telegram.update import Update

lang_translations = gettext.translation(
    "messages", localedir="locales", languages=["es"]
)
lang_translations.install()


def is_no(text):
    return text.lower() in ["no", "nop"]


def is_yes(text):
    return text.lower() in ["yes", "yep", "si", "sí"]


def is_command(text):
    return text and text.startswith("/")


def get_command_and_parameters(text: str):
    if not is_command(text):
        return None, []
    parts = text.split(" ")
    return parts[0], [item for item in parts[1:] if item != " "]


def trans(text):
    return lang_translations.gettext(text)


def reply_and_remove(text, update: Update, time_secs=3):
    bot_message = update.message.reply_text(text)
    chat_id = update.effective_chat.id
    time.sleep(time_secs)
    try:
        update.message.bot.delete_message(
            chat_id=chat_id, message_id=update.effective_message.message_id
        )
        bot_message.bot.delete_message(
            chat_id=chat_id, message_id=bot_message.message_id
        )
    except BadRequest:
        pass
