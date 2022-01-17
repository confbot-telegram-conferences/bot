from app.helpers import reply_and_remove
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
from app.core.translator import Translator
from app.utils import inject_fuction


@inject_fuction()
def commands_only_in_group(
    update: Update, context: CallbackContext, translation: Translator
):
    update.message.reply_text(translation._("commands_only_in_group"))


@inject_fuction()
def commands_only_private(
    update: Update, context: CallbackContext, translation: Translator
):
    reply_and_remove(translation._("commands_only_private"), update=update)
