import os
from app.bot_config import ConfigBotManager
from injector import inject
from injector import Injector
from telegram.ext.filters import Filters
from telegram import Update, BotCommandScopeAllGroupChats
from telegram.ext import MessageHandler, CallbackQueryHandler, CallbackContext
from app.core.filters import FilterInCommand
from app.injector import injector
from app.telegram.telegram_starter import TelegramStarter
from app.handlers2.out_of_context import commands_only_in_group, commands_only_private
from app.web import start_controllers
from .listeners import register as register_listener

bot_manager = injector.get(ConfigBotManager)


dispatcher = bot_manager.dispatcher
is_group_commands = FilterInCommand(bot_manager.get_group_commands)


class Main:
    @inject
    def __init__(self, injector: Injector):
        self.injector = injector

    def start(self):
        register_listener()
        start_controllers()


def all_messages_handler(update: Update, context: CallbackContext):
    starter = injector.get(TelegramStarter)
    starter.handle_all_messages(update, context)


def callback_query(update: Update, context: CallbackContext):
    starter = injector.get(TelegramStarter)
    starter.callback_query(update, context)


def handle_command(update: Update, context: CallbackContext):
    starter = injector.get(TelegramStarter)
    starter.handle_command(update, context)


# Dispatchers
dispatcher.add_handler(
    MessageHandler(
        Filters.private & Filters.command & ~is_group_commands,
        handle_command,
    )
)
dispatcher.add_handler(CallbackQueryHandler(callback_query))
dispatcher.add_handler(
    MessageHandler((Filters.private & ~Filters.command), all_messages_handler)
)
bot_user_name = os.getenv("TELEGRAM_BOT_NAME", "confSlider_bot")
dispatcher.add_handler(
    MessageHandler(
        (Filters.chat_type.group | Filters.chat_type.supergroup)
        & Filters.command  # noqa
        & ~is_group_commands  # noqa
        & Filters.regex(f"@{bot_user_name}"),  # noqa
        commands_only_private,
    )
)
dispatcher.add_handler(
    MessageHandler(
        Filters.private & Filters.command & is_group_commands,
        commands_only_in_group,
    )
)
my_private_commands = (
    dispatcher.get_my_commands() + bot_manager.get_my_private_commands()
)
bot_manager.bot.set_my_commands(commands=my_private_commands)
bot_manager.bot.set_my_commands(
    commands=bot_manager.get_my_group_commands(), scope=BotCommandScopeAllGroupChats()
)
