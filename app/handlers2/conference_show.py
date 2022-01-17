from telegram.parsemode import ParseMode
from app.config import Config
from app.handlers2.mixins.show_slide_mixin import ShowSlideMixin
from app.services.api.slide import SlideApiService
from injector import inject
from string import Template
from app.services.api.entities.conference import Conference
from app.core.exception import BackendException
from app.models.entities.user import User
from app.services.api.conference import ConferenceApiService
from app.helpers import get_command_and_parameters
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from app.transalation import trans as _
from blinker import signal
from app.core.callback_context import CallbackContext


class ConferenceShowManager(ShowSlideMixin):
    @inject
    def __init__(
        self,
        conference_service: ConferenceApiService,
        slide_service: SlideApiService,
        config: Config,
    ):
        self.conference_service = conference_service
        self.slide_service = slide_service
        self.config = config

    def callback(self, update: Update, context: CallbackContext):
        key, params = get_command_and_parameters(update.callback_query.data)
        update.effective_message.edit_text(**self.do_show(update, context, params[0]))

    def start(self, update: Update, context: CallbackContext, id):
        update.effective_message.reply_text(**self.do_show(update, context, id))

    def do_show(self, update: Update, context: CallbackContext, id):
        context.user_data["conference_show"] = {"conference_id": id}
        try:
            conference = self.conference_service.get_by_id(id, user=context.user)
            keyboard = [
                InlineKeyboardButton(
                    text=_("conference_show_start"),
                    callback_data="/navigate_show_conference 1",
                )
            ]
            navigate = [
                InlineKeyboardButton(
                    text=_("go_to_start_btn"), callback_data="/init_start_bot"
                )
            ]
            if conference.course:
                navigate = [
                    InlineKeyboardButton(
                        text=_("conference_show_go_to_course"),
                        callback_data=f"/show_course {conference.course['id']}",
                    )
                ] + navigate
            statistics = self.conference_service.statistics(
                conference.id, user=context.user
            ).json()
            return {
                "text": self._get_header_text(
                    conference=conference, statistics=statistics
                ),
                "reply_markup": InlineKeyboardMarkup([keyboard + navigate]),
                "parse_mode": ParseMode.MARKDOWN,
            }
        except BackendException as e:
            if e.status_code == 404:
                return {"text": "conference_show_conference_not_found"}
            raise e

    def _get_header_text(self, conference: Conference, statistics):
        return Template(_("conference_show_header_name")).substitute(
            name=conference.name,
            number_slides=conference.number_of_slides,
            description=conference.description,
            course=conference.course["name"] if conference.course else "-",
            count_unique_show=statistics["count_unique_show"],
            evaluation_avg=statistics["evaluation_avg"],
        )

    def navigate(self, update: Update, context: CallbackContext):
        key, params = get_command_and_parameters(update.callback_query.data)
        conference = self.conference_service.get_by_id(
            context.user_data["conference_show"]["conference_id"], user=context.user
        )
        return self._show_slide(int(params[0]), conference, update, context.user)

    def _show_slide(
        self, slide_number, conference: Conference, update: Update, user: User
    ):
        slide, is_last = self.conference_service.get_slide_by_position(
            user=user, conference_id=conference.id, index=slide_number
        )
        if not slide:
            return update.effective_message.reply_text(_("conference_show_empty"))
        signal("conference_show_step").send(
            self, slide=slide, user=user, conference=conference
        )
        is_first = slide_number == 1
        buttons = []
        if not is_first and not is_last:
            buttons = buttons + [
                InlineKeyboardButton(
                    text=_("conference_show_previos"),
                    callback_data=f"/navigate_show_conference {int(slide_number) - 1}",
                )
            ]
        if not is_last:
            buttons = buttons + [
                InlineKeyboardButton(
                    text=_("conference_show_abort"),
                    callback_data="/abort_conference_show",
                )
            ]
        if not is_last:
            buttons = buttons + [
                InlineKeyboardButton(
                    text=_("conference_show_next"),
                    callback_data=f"/navigate_show_conference {int(slide_number) + 1}",
                )
            ]
        self._send_slide_files(update=update, slide=slide, buttons=buttons, user=user)
        if is_last:
            buttons = [
                [
                    InlineKeyboardButton(
                        text=_(":pensive:"),
                        callback_data="/evaluate_conference 1",
                    ),
                    InlineKeyboardButton(
                        text=_(":confused:"),
                        callback_data="/evaluate_conference 2",
                    ),
                    InlineKeyboardButton(
                        text=_(":wink:"),
                        callback_data="/evaluate_conference 3",
                    ),
                    InlineKeyboardButton(
                        text=_(":smile:"),
                        callback_data="/evaluate_conference 4",
                    ),
                    InlineKeyboardButton(
                        text=_(":heart_eyes:"),
                        callback_data="/evaluate_conference 5",
                    ),
                ]
            ]
            update.effective_message.reply_text(
                text=_("conference_show_end"),
                reply_markup=InlineKeyboardMarkup(buttons),
            )

    def abort(self, update: Update, context: CallbackContext):
        conference = self.conference_service.get_by_id(
            context.user_data["conference_show"]["conference_id"], user=context.user
        )
        update.effective_message.reply_text(
            text=_("conference_show_abort_message"),
            reply_markup=InlineKeyboardMarkup(self._end_buttons(conference=conference)),
        )

    def _end_buttons(self, conference: Conference):
        share_link = self.config.get_shared_link(
            _("conference_wait_share_text") % conference.name,
            conference.share_id,
        )
        buttons = [
            InlineKeyboardButton(
                text=_("conference_show_again"),
                callback_data=f"/show_conference {conference.id}",
            ),
            InlineKeyboardButton(text=_("conference_wait_share"), url=share_link),
        ]
        buttons = []
        if conference.course:
            buttons += [
                InlineKeyboardButton(
                    text=_("conference_show_go_to_course"),
                    callback_data=f"/show_course {conference.course['id']}",
                ),
            ]
        buttons += [
            InlineKeyboardButton(
                text=_("go_to_start_btn"),
                callback_data="/init_start_bot",
            ),
        ]
        return [
            [
                InlineKeyboardButton(
                    text=_("conference_show_again"),
                    callback_data=f"/show_conference {conference.id}",
                ),
                InlineKeyboardButton(text=_("conference_wait_share"), url=share_link),
            ],
            buttons,
        ]

    def evaluate(self, update: Update, context: CallbackContext):
        conference = self.conference_service.get_by_id(
            context.user_data["conference_show"]["conference_id"], user=context.user
        )
        key, params = get_command_and_parameters(update.callback_query.data)
        self.conference_service.evaluate(
            evaluation=params[0], conference=conference, user=context.user
        )
        update.effective_message.reply_text(
            text=_("conference_show_evaluation_thanks"),
            reply_markup=InlineKeyboardMarkup(self._end_buttons(conference=conference)),
        )
