from blinker import signal
from app.utils import injector_signal
from app.core.logger import message_recieved, message_sent
from app.listernes_handlers import (
    start_command_parameter_conference,
    start_command_parameter_course,
    start_conference_in_group,
    user_conference_view_listener,
)


def register():
    signal("message_recieved").connect(message_recieved)
    signal("message_sent").connect(message_sent)
    injector_signal("start_command_parameter", start_command_parameter_conference)
    injector_signal("start_command_parameter", start_command_parameter_course)
    injector_signal("conference_show_step", user_conference_view_listener)
    injector_signal("start_conference_in_group", start_conference_in_group)
