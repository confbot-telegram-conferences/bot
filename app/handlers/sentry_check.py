from app.helpers import get_command_and_parameters
from app.request import Request
from app.core.context import Context
from app.core.handler import Handler


class SentryCheckHandler(Handler):
    def get_start_commands(self):
        return ["/sentrycheck"]

    def start(self, context: Context, request: Request):
        _, parameters = get_command_and_parameters(context.text)
        response = request.get(f"/api/sentry-check/{parameters[0]}/")
        return "Works" if response.status_code == 200 else "Error"
