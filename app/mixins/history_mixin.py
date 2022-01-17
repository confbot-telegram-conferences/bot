from app.core.context import Context


class HistoryMixin:
    def command_back_in_history(self, context: Context):
        context.user.history_pop()
        last = context.user.history_top()
        context.forward(last)

    def create_back_button(self, context: Context):
        return context.create_button(
            self._("back_in_history_btn"), callback_data="/back_in_history"
        )
