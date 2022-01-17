from app.config import Config
from string import Template
from injector import inject
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from app.services.api.entities.course import Course
from typing import Any
from app.handlers2.mixins.paginage_mixin import PaginateMixin
from app.services.api.conference import ConferenceApiService
from app.helpers import get_command_and_parameters
from telegram import Update
from app.core.callback_context import CallbackContext
from app.services.api.course import CourseApiService
from app.transalation import trans as _


class CourseShowManager(PaginateMixin):
    @inject
    def __init__(
        self,
        service: ConferenceApiService,
        course_service: CourseApiService,
        config: Config,
    ):
        self.service = service
        self.course_service = course_service
        self.config = config

    def callback(self, update: Update, context: CallbackContext):
        key, params = get_command_and_parameters(update.callback_query.data)
        update.effective_message.edit_text(**self.paginate(update, context, params[0]))

    def start(self, update: Update, context: CallbackContext, id):
        update.effective_message.reply_text(**self.paginate(update, context, id))

    def paginate(self, update: Update, context: CallbackContext, id):
        context.user_data["course_show"] = {"course_id": id}
        return self._list(update=update, context=context, page=1)

    def _get_service(self, **kwargs):
        return self.service

    def _get_list_data(self, update: Update, context: CallbackContext, **kwargs):
        service = self._get_service()
        user_data = context.user_data["course_show"]
        params = {"course": user_data["course_id"]}
        data = service.list(user=context.user, **params, **kwargs)
        context.user_data["course_show"] = {**user_data, **{"count": data["count"]}}
        return data

    def _get_item_command(self, item: Any, **kwargs):
        return f"/show_conference {str(item.id)}"

    def _callback_subfix(self, **kwargs):
        return "show_course"

    def _get_list_header(self, update: Update, context: CallbackContext, **kwargs):
        user_data = context.user_data["course_show"]
        course: Course = self.course_service.get_by_id(
            user_data["course_id"], user=context.user
        )
        return Template(_("conference_admin_list_menu_course")).substitute(
            name=course.name,
            number_of_conferences=course.number_of_active_conferences,
            description=course.description,
            count=user_data["count"],
        )

    def _extra_buttons(self, update: Update, context: CallbackContext):
        course: Course = self.course_service.get_by_id(
            context.user_data["course_show"]["course_id"], user=context.user
        )
        share_link = self.config.get_shared_link(
            _("course_wait_share_text") % course.name, course.share_id
        )
        share_button = InlineKeyboardButton(text=_("course_wait_share"), url=share_link)
        channel_id = context.user_data.get(
            "channel_active"
        )  # Some user doesn't have this value, because it needs restart the bot.
        if update.callback_query:  # It is callback query
            return [
                [share_button],
                self._get_back_buttons(
                    command_back=f"/public_courses_channel {channel_id}"
                    if channel_id
                    else ""
                ),
            ]
        return [
            [
                InlineKeyboardButton(
                    text=_("go_to_start_btn"),
                    callback_data="/init_start_bot",
                ),
                share_button,
            ]
        ]
