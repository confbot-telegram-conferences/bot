from collections import defaultdict
from copy import copy
from typing import Optional, Tuple
from injector import inject
from telegram.ext import BasePersistence
from app.models.repositories.user_repository import UserRepository
from app.telegram.telegram_context import TELEGRAM_ID_FIELD


class Data(defaultdict):
    def __init__(self, user_repository: UserRepository, _copy=None):
        if _copy is not None:
            self.__dict__ = copy(_copy.__dict__)
        self.user_repository = (
            user_repository if user_repository else _copy.user_repository
        )

    def __missing__(self, key):
        user = self.user_repository.get({TELEGRAM_ID_FIELD: key})
        value = getattr(user, "context_data", {})
        self[key] = value
        return value


class MyPersister(BasePersistence):
    @inject
    def __init__(self, user_repository: UserRepository):
        super().__init__(store_chat_data=False, store_bot_data=False)
        self.user_repository = user_repository

    def get_user_data(self):
        return Data(self.user_repository)

    def update_user_data(self, user_id, data):
        user = self.user_repository.get({TELEGRAM_ID_FIELD: user_id})
        user.context_data = data
        self.user_repository.save(user)

    def flush(self, *args, **kwargs):
        pass

    def get_bot_data(self):
        pass

    def get_chat_data(self):
        pass

    def get_conversations(self, name: str):
        return defaultdict()

    def update_bot_data(self):
        pass

    def update_chat_data(self):
        pass

    def update_conversation(
        self, name: str, key: Tuple[int, ...], new_state: Optional[object]
    ) -> None:
        pass
