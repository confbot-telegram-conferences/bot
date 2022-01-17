from app.core.context import Context
from app.core.handler import Handler


class ErrorHandler(Handler):
    def can_handler(self, text, context: Context):
        """
        This handler only will be used in the Context class when a "HandlerNotFoundException" is raised.
        """
        return False

    def handle(self, context: Context):
        context.user.clear_context()
        context.send_message(self._("fatal_error_text"))
