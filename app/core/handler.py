from app.utils import load_di_parameters
from abc import ABCMeta
from app.core.exception import HandlerNotFoundException
from app.models.entities.user import User
from injector import Injector, inject
from app.helpers import get_command_and_parameters, is_command
from .translator import Translator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Context


class Handler(metaclass=ABCMeta):
    @inject
    def __init__(self, trans: Translator, injector: Injector):
        self._ = trans
        self.ngettext = trans.ngettext
        self.injector = injector

    @classmethod
    def get_code(cls):
        return str(cls)

    def handle(self, context: "Context", **kwargs):
        text = context.text
        if self.is_start_command(context):
            return self._call_method(self.start, context, **kwargs)
        method = (
            self._get_command(text)
            if is_command(text)
            else self._get_method_by_tep(context)
        )
        return self._call_method(method, context, **kwargs)

    def _get_command(self, text: str):
        command, _ = get_command_and_parameters(text)
        method = getattr(self, f"command_{command[1:]}", None)
        if not method:
            raise HandlerNotFoundException()
        return method

    def _get_method_by_tep(self, context: "Context"):
        if not context.user.step:
            raise HandlerNotFoundException()
        method = getattr(self, context.user.step, None)
        if not method:
            raise HandlerNotFoundException()
        return method

    def _call_method(self, method, context: "Context", **kwargs):
        if getattr(method, "clear_history", False):
            context.user.clear_message_history()
        parameters = load_di_parameters(method, context=context, **kwargs)
        use_history = getattr(method, "use_history", False)
        update_last = getattr(method, "update_last", False)
        message = method(**parameters)
        if not message:
            return
        if isinstance(message, list):
            return context.send_messages(message)
        assert (
            not use_history or use_history and message
        ), "If you use use_history, you need to return a message in the method."
        message = message if isinstance(message, dict) else {"message": message}
        return context.send_message(
            use_history=use_history, update_last=update_last, **message
        )

    def _update_user_handler_data(self, user: User, data):
        handler_data = user.handler_data
        user.handler_data = {
            **handler_data,
            **data,
        }
        return user

    def is_current_handler(self, context: "Context"):
        return context.user.current_handler == self.get_code()

    def is_start_command(self, context: "Context"):
        if context.message.in_group and not self.is_group_handler(context):
            return False
        if not context.message.in_group and self.is_group_handler(context):
            return False
        command, _ = get_command_and_parameters(context.text)
        return command in self.get_start_commands()

    def is_group_handler(self, context: "Context"):
        return False

    def get_start_commands(self):
        return []

    def get_start_commands_with_description(self):
        return []

    def start(self, *args, **kwargs):
        pass
