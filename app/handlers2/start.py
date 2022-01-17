from app.models.repositories.user_repository import UserRepository
from injector import Injector, inject
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from app.core.callback_context import CallbackContext
from blinker import signal
from app.transalation import trans as _


class StartManager:
    @inject
    def __init__(self, injector: Injector, user_repository: UserRepository):
        self.injector = injector
        self.user_repository = user_repository

    def command(self, update: Update, context: CallbackContext):
        if len(context.args) == 0:
            return update.effective_message.reply_text(**self._process(update, context))
        callbacks = signal("start_command_parameter").send(
            self, parameter=context.args[0]
        )
        for key, callback in callbacks:
            if callback:
                params = {**{"update": update, "context": context}, **callback[1]}
                return callback[0](**params)

    def callback(self, update: Update, context: CallbackContext):
        update.effective_message.edit_text(**self._process(update, context))

    def _process(self, update: Update, context: CallbackContext):
        keyboard = [
            [
                InlineKeyboardButton(
                    text=_("start_channel_public"),
                    callback_data="/channel_public",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_("start_my_space"), callback_data="/myspace"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_("start_command_help"), callback_data="help"
                ),
            ],
        ]
        # It is to sopport the old logic
        context.user.last_message_id = update.effective_message.message_id
        self.user_repository.save(context.user)

        return {
            "text": _("start_command_hearder"),
            "reply_markup": InlineKeyboardMarkup(keyboard),
        }
