from telegram.ext import Filters
from app.handlers2 import ConferenceCreateManager, UpdateByZipManager, NameConversation
from . import conversation_states_constants as constants

create_conference = {
    "entry_points": {
        "commands": {
            "end": (ConferenceCreateManager, "end"),
        },
        "callback_query_handlers": {
            "/create_conference": (ConferenceCreateManager, "start"),
            "/ask_name_create_conference": (ConferenceCreateManager, "ask_name"),
            "/give_zip_create_conference": (ConferenceCreateManager, "give_zip"),
        },
    },
    "states": {
        constants.CONFERENCE_CREATE_NAME: (ConferenceCreateManager, "save_name"),
        constants.CONFERENCE_CREATE_DESCRIPTION: (
            ConferenceCreateManager,
            "save_description",
        ),
        constants.CONFERENCE_CREATE_ZIP: {
            "callback": (ConferenceCreateManager, "upload_zip"),
            "filters": Filters.document.zip,
        },
    },
}

update_conference = {
    "entry_points": {
        "commands": {
            "end": (UpdateByZipManager, "end"),
        },
        "callback_query_handlers": {
            "/update_by_zip": (UpdateByZipManager, "start"),
            "/give_zip_update_by_zip": (UpdateByZipManager, "give_zip"),
            "/start_upload_update_by_zip": (UpdateByZipManager, "start_upload"),
            "/clear_slides_update_by_zip": (UpdateByZipManager, "clear_slides"),
            "/upload_files_start_update_by_zip": (UpdateByZipManager, "start_zip"),
        },
    },
    "states": {
        constants.CONFERENCE_UPDATE_ZIP: {
            "callback": (UpdateByZipManager, "upload_zip"),
            "filters": Filters.document.zip,
        },
    },
}

change_channel_name = {
    "entry_points": {
        "callback_query_handlers": {"/channel_change_name": (NameConversation, "start")}
    },
    "states": {
        constants.CHANGE_NAME: {
            "callback": (NameConversation, "save_name"),
            "filters": Filters.text,
        },
    },
}
