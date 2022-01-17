from app.services.api.slide import SlideApiService
from app.services.api.entities.slide import Slide
from app.core.context import Context


class ShowSlideMixin:
    def show_slide(
        self,
        context: Context,
        slide: Slide,
        slide_service: SlideApiService,
        buttons=None,
    ):
        context.send_message(
            self._("conference_create_slide_header")
            % f"{slide.position}/{slide.conference_number_of_slides}"
        )
        if slide.image_id:
            slide_service.send_image(
                user=context.user, chat_id=context.chat_id, slide=slide
            )
        if slide.voice_id:
            slide_service.send_audio(
                user=context.user, chat_id=context.chat_id, slide=slide
            )
        if buttons:
            text = slide.text if slide.text else "Menu"
            return context.send_buttons(text, [buttons])
        if slide.text:
            context.send_message(slide.text)
