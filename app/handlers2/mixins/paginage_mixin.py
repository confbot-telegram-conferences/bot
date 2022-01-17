from abc import ABCMeta, abstractmethod
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from app.handlers2.mixins.back_buttons_mixin import BackButtonsMixin
from typing import Any
from app.helpers import get_command_and_parameters
from app.transalation import trans as _
from app.core.callback_context import CallbackContext


class PaginateMixin(BackButtonsMixin, metaclass=ABCMeta):

    PAGE_SIZE = 5

    @abstractmethod
    def _get_service(self, **kwargs):
        pass

    @abstractmethod
    def _get_item_command(self, item: Any, **kwargs):
        pass

    def _get_create_command(self, **kwargs):
        pass

    @abstractmethod
    def _get_list_header(self, **kwargs):
        pass

    @abstractmethod
    def _callback_subfix(self, **kwargs):
        pass

    def _get_list_data(self, update: Update, context: CallbackContext, **kwargs):
        service = self._get_service()
        return service.list(user=context.user, **kwargs)

    def _list_out(self, **kwargs):
        return "/init_start_bot"

    def paginate(self, update: Update, context: CallbackContext):
        return self._list(page=1, update=update, context=context)

    def _button_item(self, item: Any):
        return InlineKeyboardButton(
            text=str(item),
            callback_data=self._get_item_command(item),
        )

    def _empty_list_text(self):
        return _("list_empty")

    def _list(self, page, update: Update, context: CallbackContext):
        data = self._get_list_data(
            context=context,
            update=update,
            params={"page": page, "page_size": self.PAGE_SIZE},
        )
        buttons = []
        if len(data["results"]) > 0:
            buttons += [[self._button_item(item)] for item in data["results"]]
        navigate = []
        if data["previous"]:
            navigate += [
                InlineKeyboardButton(
                    text=_("list_previous"),
                    callback_data=f"/navigate_{self._callback_subfix()} {int(page) - 1}",
                )
            ]
        if data["next"]:
            navigate += [
                InlineKeyboardButton(
                    text=_("list_next"),
                    callback_data=f"/navigate_{self._callback_subfix()} {int(page) + 1}",
                )
            ]
        if len(navigate):
            buttons += [navigate]
        buttons += self._extra_buttons(context=context, update=update)
        if not buttons:
            return {"text": self._empty_list_text()}
        return {
            "text": self._get_list_header(context=context, update=update, data=data),
            "reply_markup": InlineKeyboardMarkup(buttons),
            "parse_mode": ParseMode.MARKDOWN,
        }

    def _create_button(self, context: CallbackContext):
        return InlineKeyboardButton(
            text=_("list_create"),
            callback_data=self._get_create_command(context=context),
        )

    def _extra_buttons(self, update: Update, context: CallbackContext):
        command_back = self._list_out(context=context)
        return [
            [self._create_button(context=context)],
            self._get_back_buttons(command_back=command_back),
        ]

    def navigate(self, update: Update, context: CallbackContext):
        key, params = get_command_and_parameters(update.callback_query.data)
        update.effective_message.edit_text(
            **self._list(update=update, context=context, page=params[0])
        )
