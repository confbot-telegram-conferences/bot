from app.core.context import Context


class YesNoButtonsMixin:
    def _yes_no_buttons(self, context: Context):
        return [
            context.create_button(
                self._("Yes"),
                callback_data="yes",
            ),
            context.create_button(
                self._("No"),
                callback_data="no",
            ),
        ]
