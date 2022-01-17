from injector import inject
from telegram.inline.inlinequeryresultarticle import InlineQueryResultArticle
from telegram.inline.inputtextmessagecontent import InputTextMessageContent
from app.config import Config
from app.services.api.conference_admin import ConferenceAdminApiService
from telegram import Update
from app.core.callback_context import CallbackContext

CANT_CHARACTERS = 90


class InlineQueryManager:
    @inject
    def __init__(self, conference_service: ConferenceAdminApiService, config: Config):
        self.conference_service = conference_service
        self.config = config

    def __call__(self, update: Update, context: CallbackContext):
        query = update.inline_query.query
        objects = self.conference_service.list(
            user=context.user, params={"search": query}
        )
        results = [self._inline_result(item) for item in objects["results"]]
        update.inline_query.answer(results)

    def _inline_result(self, item):
        description = item.description if item.description else ""
        description = (
            description
            if len(description) <= CANT_CHARACTERS
            else description[0:CANT_CHARACTERS] + " ..."
        )
        data = {
            "id": item.id,
            "title": item.name,
            "input_message_content": InputTextMessageContent(
                f"/show_c@{self.config.TELEGRAM_BOT_NAME} {item.id}"
            ),
            "description": description,
        }
        return InlineQueryResultArticle(**data)
