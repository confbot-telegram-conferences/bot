from app.helpers import get_command_and_parameters
from app.core.context import Context


class ForwardMixin:
    def command_forward(self, context: Context):
        _, parameters = get_command_and_parameters(context.text)
        command = " ".join(parameters)
        context.forward(f"/{command}")

    def forward_new_handler(self, text, context: Context):
        context.user.clear_context()
        context.forward(text)

    def command_f_clear(self, context: Context):
        context.user.clear_context()
        return self.command_forward(context=context)
