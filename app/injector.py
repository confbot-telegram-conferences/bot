from flask import Flask
from telegram import Bot
from telegram.utils.request import Request
from injector import Binder, Injector, Module, singleton
from app.utils import load_handlers
from app.config import Config
from app import handlers


class MyModule(Module):
    def configure(self, binder: Binder):
        _handlers = load_handlers(handlers)
        config = Config(_handlers)
        app = Flask(config.SERVICE_NAME)
        binder.bind(Config, to=config, scope=singleton)
        binder.bind(Flask, to=app, scope=singleton)
        self._configure_bot(binder=binder, config=config)

    def _configure_bot(self, binder: Binder, config: Config):
        bot = Bot(config.TELEGRAM_TOKEN, request=Request(con_pool_size=10))
        binder.bind(Bot, to=bot, scope=singleton)


injector = Injector([MyModule()])
