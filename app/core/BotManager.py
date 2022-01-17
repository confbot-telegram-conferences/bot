from typing import Dict, List
from injector import Injector, inject
from telegram.bot import Bot
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Updater,
    Filters,
)
from app.core.dispatcher import Dispatcher


class BotManager:
    @inject
    def __init__(self, injector: Injector, dispatcher: Dispatcher, bot: Bot):
        self.dispatcher = dispatcher
        self.bot = bot
        self.injector = injector
        self.updater = Updater(dispatcher=dispatcher, workers=None)
        self.dispatcher = self.updater.dispatcher
        self._start_init()

    def __call__(self, url=None, polling=False, token=None, port=5000):
        if polling:
            self.updater.start_polling()
        else:
            self.updater.start_webhook(
                listen="0.0.0.0", port=port, url_path=token, webhook_url=url
            )
            self.updater.idle()

    def _start_init(self):
        self._init_commands()
        self.get_inline_query()
        self._init_conversations()
        self._init_callback_query_handlers()
        self._start_messages()

    def _start_messages(self):
        for filters, callback in self.get_message_config():
            self.dispatcher.add_handler(
                MessageHandler(filters, self._get_callback(callback))
            )

    def _init_commands(self):
        filter_group = Filters.chat_type.group | Filters.chat_type.supergroup
        self._retister_command_handlers(
            self.get_group_commands_config(), filters=filter_group
        )
        self._retister_command_handlers(
            self.get_private_commands_config(), filters=Filters.chat_type.private
        )

    def _init_callback_query_handlers(self):
        for key, value in self.get_callback_query_handlers_config().items():
            self.dispatcher.add_handler(
                CallbackQueryHandler(self._get_callback(value), pattern=key)
            )

    def _init_conversations(self):
        for item in self.get_conversations_config():
            self.dispatcher.add_handler(self._init_conversation(item))

    def _init_conversation(self, config):
        assert not (
            "entry_points" not in config or "states" not in config
        ), "conversation config needs to have entry_points and states"
        entry_points = []
        if "callback_query_handlers" in config["entry_points"]:
            entry_points += [
                self._create_callback_query_handler(callback=item, pattern=key)
                for key, item in config["entry_points"][
                    "callback_query_handlers"
                ].items()
            ]
        if "commands" in config["entry_points"]:
            entry_points += [
                self._create_command_handler(key, value)
                for key, value in config["entry_points"]["commands"].items()
            ]
        states = {}
        default_filters = Filters.text & ~Filters.command
        for key, item in config["states"].items():
            callback = item
            filters = default_filters
            if isinstance(item, dict):
                filters = item["filters"] if "filters" in item else filters
                callback = item["callback"]
            states[key] = [MessageHandler(filters, self._get_callback(callback))]
        return ConversationHandler(
            entry_points=entry_points, states=states, fallbacks=entry_points
        )

    def get_inline_query(self) -> None:
        pass

    def _retister_command_handlers(self, command_config, **kwargs):
        for key, value in command_config.items():
            self.dispatcher.add_handler(
                self._create_command_handler(key, value, **kwargs)
            )

    def _create_command_handler(self, command, config, **kwargs):
        if isinstance(config, tuple):
            config = {"callback": config}
        callback = config["callback"]
        config["callback"] = self._get_callback(callback)
        data = {**kwargs, **config}
        if "description" in data:
            del data["description"]
        return CommandHandler(command=command, **data)

    def _create_callback_query_handler(self, callback, **kwargs):
        if isinstance(callback, tuple):
            callback = self._get_callback(callback)
        return CallbackQueryHandler(callback=callback, **kwargs)

    def _get_callback(self, data):
        if isinstance(data, tuple):
            return getattr(self.injector.get(data[0]), data[1])
        return data

    def get_command_description(self) -> None:
        commands = {
            **self.get_group_commands_config(),
            **self.get_private_commands_config(),
        }
        return [
            (key, value["description"])
            for key, value in commands.items()
            if "description" in value
        ]

    def _filter_my_commands(self, commands):
        return [
            (key, value["description"])
            for key, value in commands.items()
            if "description" in value
        ]

    def get_my_private_commands(self):
        return self._filter_my_commands(self.get_private_commands_config())

    def get_my_group_commands(self):
        return self._filter_my_commands(self.get_group_commands_config())

    @property
    def get_group_commands(self) -> List:
        return [f"/{key}" for key, _ in self.get_group_commands_config().items()]

    def get_group_commands_config(self) -> Dict:
        return {}

    def get_private_commands_config(self) -> Dict:
        return {}

    def get_conversations_config(self) -> Dict:
        return []

    def get_callback_query_handlers_config(self):
        return {}

    def get_message_config(self):
        return []
