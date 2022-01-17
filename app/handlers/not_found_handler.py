from app.core.context import Context
from app.core.handler import Handler


class NotFoundHandler(Handler):
    def can_handler(self, text, context: Context):
        """
        This handler only will be used in the Context class when a "HandlerNotFoundException" is raised.
        """
        return False

    def handle(self, context: Context, message=None):
        context.user.clear_context()
        message = message if message else self._("no_found_text")
        context.send_message(message)
