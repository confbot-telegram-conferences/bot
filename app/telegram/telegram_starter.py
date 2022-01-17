from injector import Injector, inject
from telegram.update import Update
from telegram.ext import CallbackContext
from app.config import Config
from app.core.context import MessageContext, UserContext
from app.telegram.telegram_context import TelegramContext


class TelegramStarter:
    @inject
    def __init__(self, injector: Injector, config: Config):
        self.injector = injector
        self.config = config

    def callback_query(self, update: Update, context: CallbackContext):
        data = update.to_dict()
        query = data["callback_query"]
        self.process(
            query["data"],
            query["from"]["id"],
            query["from"],
            update,
            context.bot,
        )

    def handle_command(self, update: Update, context: CallbackContext):
        data = update.to_dict()
        self.process(
            update.message.text,
            update.effective_chat.id,
            data["message"]["from"],
            update,
            context.bot,
        )

    def handle_all_messages(self, update: Update, context: CallbackContext):
        data = update.to_dict()
        self.process(
            update.message.text,
            update.effective_chat.id,
            data["message"]["from"],
            update,
            context.bot,
        )

    def process(self, text, chat_id, user_data, t_update: Update, bot):
        data = t_update.to_dict()
        message = MessageContext(text=text, in_group=False)
        context = self.injector.create_object(
            TelegramContext,
            dict(
                chat_id=chat_id,
                bot=bot,
                message=message,
                user_context=self.get_user(user_data),
                input=data,
                t_update=t_update,
                original_handler=t_update,
            ),
        )
        context()

    def get_user(self, user):
        return UserContext(
            id=user["id"] if "id" in user else None,
            first_name=user["first_name"] if "first_name" in user else None,
            last_name=user["last_name"] if "last_name" in user else None,
            is_bot=user["is_bot"] if "is_bot" in user else None,
            language_code=user["language_code"] if "language_code" in user else None,
        )
