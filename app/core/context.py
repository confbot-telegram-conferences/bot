from telegram.update import Update
from app.models.entities.user import User
from app.helpers import is_command, trans as _
from typing import Any
from blinker import signal
from collections import namedtuple
from abc import ABCMeta, abstractmethod
from app.models.repositories import UserRepository
from injector import Injector, inject
from .exception import (
    AbortProcessException,
    BadBotRequestException,
    HandlerNotFoundException,
)
from app.config import Config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Handler

UserContext = namedtuple("UserContext", "id first_name last_name is_bot language_code")
MessageContext = namedtuple("MessageContext", "text in_group")


class Context(metaclass=ABCMeta):
    @inject
    def __init__(
        self,
        injector: Injector = None,
        config: Config = None,
        user_repository: UserRepository = None,
        bot: Any = None,
        chat_id: Any = None,
        message: MessageContext = None,
        user_context: UserContext = None,
        input: Any = None,
        original_handler: Any = None,
        t_update: Update = None,
    ):
        self.config = config
        self.t_update = t_update
        self.injector = injector
        self.user_repository = user_repository
        self.bot = bot
        self.chat_id = chat_id
        self.message = message
        self.user_context = user_context
        self.input = input
        self.original_handler = original_handler
        self.user: User = self.get_user()

    def __call__(self) -> None:
        try:
            self._handle()
        except AbortProcessException as e:
            from app.handlers import NotFoundHandler

            self.injector.get(NotFoundHandler).handle(context=self, message=e.message)
        except HandlerNotFoundException:
            from app.handlers import NotFoundHandler

            message = self._get_message_command_out_of_context(self.text)
            self.injector.get(NotFoundHandler).handle(context=self, message=message)
        except Exception as e:
            raise e
        self.user_repository.update(self.user)  # Save any data updated in the user

    def _get_message_command_out_of_context(self, text):
        if not is_command(text):
            return
        return (
            _("command_out_of_context_private")
            if self.message.in_group
            else _("command_out_of_context_group")
        )

    def __repr__(self) -> str:
        return f"<Context message={self.message} user_context={self.user_context} input={self.input}>"

    def _handle(self) -> None:
        handler = self.get_by_start_command()
        if not handler:
            handler = self.get_current_handler()
        if handler:
            handler.handle(context=self)
        else:
            raise HandlerNotFoundException()

    def _loop_handler(self, check):
        for handler_class in self.config.handlers:
            handler = self.injector.get(handler_class)
            result = check(handler)
            if result:
                return result

    def get_by_start_command(self) -> "Handler":
        return self._loop_handler(
            lambda handler: handler if handler.is_start_command(self) else None
        )

    def get_current_handler(self) -> "Handler":
        return self._loop_handler(
            lambda handler: handler if handler.is_current_handler(self) else None
        )

    def send_message(self, message, use_history=False, update_last=False, **kwargs):
        signal("message_sent").send(self, texts=message)
        if use_history:
            new_message = self._message_history(message, **kwargs)
        elif update_last:
            new_message = self.update_last_message(message, **kwargs)
        else:
            self.user.clear_message_history()
            new_message = self._send_message(message, **kwargs)
        self.user.last_message_id = new_message["message_id"]
        return new_message

    def _message_history(self, message, **kwargs):
        self.user.add_to_history(self.text)
        try:
            new_message = self.update_last_message(message, **kwargs)
        except BadBotRequestException:
            new_message = self._send_message(message, **kwargs)
        return new_message

    def update_last_message(self, message, **kwargs):
        return self._update_message(
            message, message_id=self.user.last_message_id, **kwargs
        )

    def delete_last_message(self):
        self.delete_message(self.user.last_message_id)

    def forward(self, text):
        self.message = MessageContext(text=text, in_group=False)
        self.__call__()

    def send_messages(self, messages, **kwargs):
        for text in messages:
            self.send_message(text, **kwargs)

    @abstractmethod
    def delete_message(self, message_id):
        pass

    @abstractmethod
    def send_buttons(self, buttons, **kwargs):
        pass

    @abstractmethod
    def build_buttons(self, buttons, **kwargs):
        pass

    def send_photo(self, photo):
        return self._send_photo(open(photo, "rb"))

    def send_voice(self, voice):
        return self._send_voice(open(voice, "rb"))

    @abstractmethod
    def _send_message(self, text):
        pass

    @abstractmethod
    def _update_message(self, text):
        pass

    @abstractmethod
    def _send_photo(self, photo):
        pass

    @abstractmethod
    def _send_voice(self, voice):
        pass

    @abstractmethod
    def get_user(self):
        pass

    @abstractmethod
    def get_image(self):
        pass

    @abstractmethod
    def get_voice(self):
        pass

    @abstractmethod
    def get_audio(self):
        pass

    @abstractmethod
    def get_document(self):
        pass

    @abstractmethod
    def create_button(self, text, callback):
        pass

    @property
    def text(self):
        return self.get_text()

    @abstractmethod
    def get_text(self) -> str:
        pass
