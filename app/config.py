import os
import urllib


class Config:
    SERVICE_NAME = os.getenv("SERVICE_NAME", "CONFERENCE_BOT")
    MONGO_CONECTION = os.getenv("MONGO_CONECTION")
    DATABASE = os.getenv("MONGO_DATABASE")
    APP_ENV = os.getenv("APP_ENV", "development")
    TELEGRAM_POLLING = os.getenv("TELEGRAM_POLLING", False)
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME", "confSlider_bot")
    APP_HOST = os.getenv("APP_HOST")
    APP_PORT = os.getenv("APP_PORT", 5000)
    APP_KEY = os.getenv("APP_KEY")
    BACKEND_URL = os.getenv("BACKEND_URL")
    ZIP_MAX_SIZE = 20971520

    def __init__(self, handlers):
        self.handlers = handlers

    def get_shared_url(self, id):
        return f"https://t.me/{self.TELEGRAM_BOT_NAME}?start={id}"

    def get_shared_link(self, text, id):
        shared_link = urllib.parse.urlencode(
            {"text": text, "url": self.get_shared_url(id)}
        )
        return f"tg://msg_url?{shared_link}"

    @property
    def zip_max_size(self):
        return self.ZIP_MAX_SIZE / 1024 / 1024
