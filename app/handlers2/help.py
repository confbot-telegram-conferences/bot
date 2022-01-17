from app.handlers2.mixins.back_buttons_mixin import BackButtonsMixin
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from app.transalation import trans as _


class HelpManager(BackButtonsMixin):
    def command(self, update: Update, context: CallbackContext):
        update.effective_message.reply_text(**self._process_message(update, context))

    def callback(self, update: Update, context: CallbackContext):
        update.effective_message.edit_text(**self._process_message(update, context))

    def _process_message(self, update: Update, context: CallbackContext):
        keyboard = self._get_back_buttons(command_back="/init_start_bot")
        return {
            "text": _("bot_help"),
            "reply_markup": InlineKeyboardMarkup([keyboard]),
        }
