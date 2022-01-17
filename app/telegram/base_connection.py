from app.helpers import get_command_and_parameters, is_command
from telegram import Update
from app.telegram.telegram_context import TelegramContext
from app.core.context import MessageContext, UserContext
from app.config import Config
from injector import Injector, inject


class BaseConnection:
    @inject
    def __init__(self, injector: Injector, config: Config):
        self.injector = injector
        self.config = config

    def process(self, text, chat_id, user_data, t_update: Update, bot):
        data = t_update.to_dict()
        message = self.get_message(text, t_update)
        if not message:
            return
        context = self.injector.create_object(
            TelegramContext,
            dict(
                chat_id=chat_id,
                bot=bot,
                message=message,
                user_context=self.get_user(user_data),
                input=data,
                original_handler=t_update,
            ),
        )
        context()

    def get_message(self, text, t_update: Update):
        command, in_group = self.get_command_and_if_in_group(text)
        message = MessageContext(text=command, in_group=in_group)
        chat_type = t_update.effective_chat.type if t_update.effective_chat else None
        if chat_type == "group" and not is_command(
            command
        ):  # In group only respond commands
            return None
        return message

    def get_command_and_if_in_group(self, text):
        command, parameters = get_command_and_parameters(text)
        if not command:
            return text, False
        parts = command.split("@")
        if len(parts) == 1:
            return text, False
        return f"{parts[0]} {' '.join(parameters)}", True

    def get_user(self, user):
        return UserContext(
            id=user["id"] if "id" in user else None,
            first_name=user["first_name"] if "first_name" in user else None,
            last_name=user["last_name"] if "last_name" in user else None,
            is_bot=user["is_bot"] if "is_bot" in user else None,
            language_code=user["language_code"] if "language_code" in user else None,
        )
