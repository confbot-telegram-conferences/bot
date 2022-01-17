import telegram
from flask import Flask, request
from injector import Injector, inject
from app.config import Config
from app.telegram.base_connection import BaseConnection
from blinker import signal


class WebHook(BaseConnection):
    @inject
    def __init__(self, injector: Injector, config: Config, flask: Flask):
        super().__init__(injector, config)
        self.flask = flask

    def callback_query(self, data, t_update):
        query = data["callback_query"]
        return {
            "text": query["data"],
            "user_data": query["from"],
            "chat_id": t_update.effective_chat.id,
        }

    def inline_query(self, data):
        query = data["inline_query"]
        return {
            "text": f"/query {query['query']}",
            "user_data": query["from"],
            "chat_id": None,
        }

    def message(self, data):
        query = data["message"]
        data = {
            "user_data": query["from"],
            "chat_id": query["chat"]["id"],
        }
        # The @ is concatenated to mark the command as a command group.
        if len(query.get("new_chat_members", [])):
            return {**{"text": "/new_members@"}, **data}
        if query.get("left_chat_member", None):
            return {**{"text": "/left_chat_member@"}, **data}
        return {**{"text": query.get("text")}, **data}

    def __call__(self):
        bot = telegram.Bot(token=self.config.TELEGRAM_TOKEN)

        def web_hook():
            t_update = telegram.Update.de_json(request.get_json(force=True), bot)
            data = t_update.to_dict()
            signal("message_recieved").send(self, update=data)
            if "callback_query" in data:
                data = self.callback_query(data, t_update)
            elif "inline_query" in data:
                data = self.inline_query(data)
            elif "message" in data:
                data = self.message(data)
            else:
                return "ok"
            self.process(t_update=t_update, bot=bot, **data)
            return "ok"

        uri = f"/telegram/webhook/{self.config.TELEGRAM_TOKEN}"
        self.flask.add_url_rule(uri, view_func=web_hook, methods=["POST"])
        url = f"{self.config.APP_HOST}{uri}"
        s = bot.setWebhook(url)
        print(
            f"The webhook was registered in this url: {url}"
            if s
            else "ERROR => The webhook wasn't registered"
        )
