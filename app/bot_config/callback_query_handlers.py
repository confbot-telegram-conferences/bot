from app.handlers2 import (
    HelpManager,
    ConferenceShowManager,
    CourseShowManager,
    StartManager,
    AlertsManager,
    StatisticsManager,
    PublishManager,
    ChannelManager,
    ChannelDetailManager,
    ChannelPublicManager,
    CourseListManager,
    ConferenceListManager,
)


callback_query_handlers = {
    "help": (HelpManager, "callback"),
    "/init_start_bot": (StartManager, "callback"),
    # Show Conference
    "/show_conference": (ConferenceShowManager, "callback"),
    "/navigate_show_conference": (ConferenceShowManager, "navigate"),
    "/abort_conference_show": (ConferenceShowManager, "abort"),
    "/evaluate_conference": (ConferenceShowManager, "evaluate"),
    "/conference_statistics": (StatisticsManager, "callback"),
    "/conference_alert_start": (AlertsManager, "callback"),
    "/conference_alert_do_start": (AlertsManager, "activate_desactivate"),
    # Show course
    "/show_course": (CourseShowManager, "callback"),
    "/init_show_course": (CourseShowManager, "callback"),
    "/navigate_show_course": (CourseShowManager, "navigate"),
    # Channel
    "/myspace": (ChannelManager, "callback"),
    "/channel_publish_start": (PublishManager, "callback"),
    "/channel_publish_do_start": (PublishManager, "activate_desactivate"),
    # Public channel
    "/channel_public": (ChannelPublicManager, "callback"),
    "/navigate_channel_public": (ChannelPublicManager, "navigate"),
    # channel detail
    "/channel_detail": (ChannelDetailManager, "callback"),
    # course channel
    "/public_courses_channel": (CourseListManager, "callback"),
    "/navigate_channel_courses": (CourseListManager, "navigate"),
    # conference channel
    "/channel_conferences": (ConferenceListManager, "callback"),
    "/navigate_channel_conferences": (ConferenceListManager, "navigate"),
}
