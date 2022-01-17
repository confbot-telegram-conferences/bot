from telegram.ext import CallbackContext, ConversationHandler
from app.transalation import trans as _
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode


class UploadZipMixin:
    def give_zip(self, update: Update, context: CallbackContext):
        file = file = open("templates/Template1.zip", "rb")
        update.effective_message.bot.send_document(
            chat_id=update.effective_chat.id, document=file
        )
        return ConversationHandler.END

    def upload_zip(self, update: Update, context: CallbackContext):
        document = update.message.document
        if document.file_size >= self.config.ZIP_MAX_SIZE:
            update.message.reply_text(
                _("conference_wait_zip_max_size") % self.config.zip_max_size
            )
            return self.ZIP
        conference_id = context.user_data["create_or_update_conference"][
            "conference_id"
        ]
        self.conference_service.upload_zip_file(
            file_data=document.to_dict(),
            user=update.model_user,
            conference=conference_id,
        )
        return self.ZIP

    def end(self, update: Update, context: CallbackContext) -> int:
        conference_id = context.user_data["create_or_update_conference"][
            "conference_id"
        ]
        keyboard = [
            [
                InlineKeyboardButton(
                    _("conference_wait_end_detail"),
                    callback_data=f"/conference {conference_id}",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            _("conference_wait_end"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        return ConversationHandler.END
