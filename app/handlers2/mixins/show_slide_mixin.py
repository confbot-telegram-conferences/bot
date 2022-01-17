from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from app.models.entities.user import User
from telegram import Update
from app.services.api.entities.slide import Slide
from app.transalation import trans as _


class ShowSlideMixin:
    def _send_slide_files(self, update: Update, slide: Slide, user: User, buttons=None):
        text = (
            _("conference_create_slide_header")
            % f"{slide.position}/{slide.conference_number_of_slides}"
        )
        chat_id = update.effective_chat.id
        update.effective_message.bot.send_message(text=text, chat_id=chat_id)
        if slide.image_id:
            self.slide_service.send_image(user=user, chat_id=chat_id, slide=slide)
        if slide.voice_id:
            self.slide_service.send_audio(user=user, chat_id=chat_id, slide=slide)
        if buttons:
            text = slide.text if slide.text else "Menu"
            return update.effective_message.bot.send_message(
                text=text,
                chat_id=chat_id,
                reply_markup=InlineKeyboardMarkup([buttons]),
            )
        if slide.text:
            update.effective_message.bot.send_message(text=slide.text, chat_id=chat_id)
