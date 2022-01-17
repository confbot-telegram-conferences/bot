from telegram import InlineKeyboardButton
from app.transalation import trans as _


class BackButtonsMixin:
    def _get_back_buttons(self, command_back):
        button_start = InlineKeyboardButton(
            text=_("go_to_start_btn"), callback_data="/init_start_bot"
        )
        return (
            [
                InlineKeyboardButton(
                    text=_("back_in_history_btn"), callback_data=command_back
                ),
                button_start,
            ]
            if command_back
            else [button_start]
        )
