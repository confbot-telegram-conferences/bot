from telegram import Update
from app.telegram.base_connection import BaseConnection
from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    InlineQueryHandler,
)


class Polling(BaseConnection):
    def __call__(self):
        updater = Updater(token=self.config.TELEGRAM_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        def message(t_update, t_context):
            data = t_update.to_dict()
            self.process(
                t_update.message.text,
                t_update.effective_chat.id,
                data["message"]["from"],
                t_update,
                t_context.bot,
            )

        def callback_query(t_update, t_context):
            data = t_update.to_dict()
            query = data["callback_query"]
            self.process(
                query["data"],
                query["from"]["id"],
                query["from"],
                t_update,
                t_context.bot,
            )

        def query(t_update: Update, t_context):
            data = t_update.to_dict()
            query = data["inline_query"]
            self.process(
                text=f"/query {query['query']}",
                user_data=query["from"],
                t_update=t_update,
                bot=t_context.bot,
            )

        dispatcher.add_handler(InlineQueryHandler(query))
        dispatcher.add_handler(MessageHandler(Filters.all, message))
        dispatcher.add_handler(CallbackQueryHandler(callback_query))

        updater.start_polling()
