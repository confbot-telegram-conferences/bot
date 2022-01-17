import logging

from injector import Injector
from telegram import Update
from app.services.api.entities.group_channel import GroupChannel
from app.handlers2 import ConferenceShowManager, CourseShowManager
from app.services.api.group_channel_admin import GroupChannelAdminApiService
from app.services.api.entities.course import Course
from app.services.api.slide import SlideApiService
from app.services.api.entities.conference import Conference
from app.services.api.entities.slide import Slide
from app.models.entities import User


def user_conference_view_listener(
    sender,
    slide: Slide,
    user: User,
    conference: Conference,
    slide_service: SlideApiService,
):
    slide_service.set_as_viewed(user=user, conference=conference, slide=slide)


def start_command_parameter_conference(
    sender, parameter, injector: Injector, *args, **kwargs
):
    id = Conference.get_share_id(parameter)
    callback = (getattr(injector.get(ConferenceShowManager), "start"), {"id": id})
    return callback if id else None


def start_command_parameter_course(
    sender, parameter, injector: Injector, *args, **kwargs
):
    id = Course.get_share_id(parameter)
    callback = (getattr(injector.get(CourseShowManager), "start"), {"id": id})
    return callback if id else None


def start_conference_in_group(
    sender,
    conference: Conference,
    user: User,
    update: Update,
    group_channel_service: GroupChannelAdminApiService,
):
    try:
        group_data = {
            **update.effective_chat.to_dict(),
            **{"external_id": update.effective_chat.id},
        }
        del group_data["id"]
        group_channel = group_channel_service.save(
            GroupChannel(**group_data), user=user
        )
        group_channel_service.start_conference(
            user=user, conference=conference, group_channel=group_channel
        )
    except Exception as e:
        logger = logging.getLogger("sentry_sdk")
        logger.exception(e)
