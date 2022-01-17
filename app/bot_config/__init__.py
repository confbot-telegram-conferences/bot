from app.handlers2 import error_handler, InlineQueryManager
from telegram.ext import InlineQueryHandler
from app.core.BotManager import BotManager
from .commands import group_commands, private_commands
from .callback_query_handlers import callback_query_handlers
from .message import messages


class ConfigBotManager(BotManager):
    def get_inline_query(self) -> None:
        handler = self.injector.get(InlineQueryManager)
        self.dispatcher.add_handler(InlineQueryHandler(handler))

    def get_callback_query_handlers_config(self):
        return callback_query_handlers

    def get_group_commands_config(self):
        return group_commands

    def get_private_commands_config(self):
        return private_commands

    def get_conversations_config(self):
        from .conversation import (
            create_conference,
            update_conference,
            change_channel_name,
        )

        return [create_conference, update_conference, change_channel_name]

    def _start_init(self):
        super()._start_init()
        self.dispatcher.add_error_handler(error_handler)

    def get_message_config(self):
        return messages
