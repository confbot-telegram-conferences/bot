from app.core.context import Context


class BackButtonsMixin:
    def _get_back_buttons(self, command_back, context: Context):
        return [
            context.create_button(
                self._("back_in_history_btn"),
                callback_data=command_back,
            ),
            context.create_button(
                self._("go_to_start_btn"),
                callback_data="/init_start_bot",
            ),
        ]
