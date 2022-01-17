import logging

from telegram import Update
from telegram.ext import CallbackContext
from app.utils import inject_fuction
from app.core.translator import Translator

logger = logging.getLogger("sentry_sdk")


@inject_fuction()
def error_handler(update: Update, context: CallbackContext, translation: Translator):
    logger.exception(context.error)
    update.effective_message.reply_text(translation._("fatal_error_text"))
