from app.handlers2.start import StartManager
from app.handlers2 import ShowInGroupManager, HelpManager
from telegram.ext.filters import Filters
from app.transalation import trans as _


filter_group = Filters.chat_type.group | Filters.chat_type.supergroup

group_commands = {
    "show_c": {"callback": (ShowInGroupManager, "start")},
    "next_slide": {
        "callback": (ShowInGroupManager, "next"),
        "description": _("conference_group_show_next_command_description"),
    },
    "show_same_slide": {
        "callback": (ShowInGroupManager, "show_same"),
        "description": _("conference_group_show_show_same_command_description"),
    },
    "close_conference": {
        "callback": (ShowInGroupManager, "close_conference"),
        "description": _("conference_group_show_reset_command_description"),
    },
}

private_commands = {
    "help": {
        "callback": (HelpManager, "command"),
        "description": _("help_command_description"),
    },
    "start": {
        "callback": (StartManager, "command"),
        "description": _("start_command_description"),
    },
}
