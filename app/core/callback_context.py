from typing import TYPE_CHECKING
from telegram.ext import CallbackContext as BaseCallbackContext

if TYPE_CHECKING:
    from .dispatcher import Dispatcher


class CallbackContext(BaseCallbackContext):
    def __init__(self, dispatcher: "Dispatcher"):
        super().__init__(dispatcher)
        self._user = None

    @property
    def user(self):
        return self._user

    @classmethod
    def from_update(cls, update: object, dispatcher: "Dispatcher") -> "CallbackContext":
        context = super().from_update(update, dispatcher)
        context._user = dispatcher.user
        return context
