from abc import ABCMeta, abstractmethod
from app.mixins.back_buttons_mixin import BackButtonsMixin
from typing import Any
from app.helpers import get_command_and_parameters
from app.core.context import Context


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

    def _load_parameters(self, context: Context, **kwargs):
        pass

    def _get_list_data(self, context: Context, **kwargs):
        service = self._get_service()
        return service.list(context.user, **kwargs)

    def _list_out(self, **kwargs):
        return "/start"

    def start(self, context: Context, **kwargs):
        context.user.current_handler = self.get_code()
        self._load_parameters(context)
        return self._list(page=1, context=context, **kwargs)

    start.use_history = True

    def _button_item(self, item: Any, context: Context):
        return context.create_button(
            str(item), callback_data=self._get_item_command(item)
        )

    def _empty_list_text(self):
        return self._("list_empty")

    def _list(self, page, context: Context, **kwargs):
        data = self._get_list_data(
            context, params={"page": page, "page_size": self.PAGE_SIZE}
        )
        buttons = []
        if len(data["results"]) > 0:
            buttons += [[self._button_item(item, context)] for item in data["results"]]
        navigate = []
        if data["previous"]:
            navigate += [
                context.create_button(
                    self._("list_previous"),
                    callback_data=f"/navigate {int(page) - 1}",
                )
            ]
        if data["next"]:
            navigate += [
                context.create_button(
                    self._("list_next"),
                    callback_data=f"/navigate {int(page) + 1}",
                )
            ]
        if len(navigate):
            buttons += [navigate]
        buttons += self._extra_buttons(context=context)
        if not buttons:
            return self._empty_list_text()
        return context.build_buttons(
            buttons, message=self._get_list_header(context=context)
        )

    def _create_button(self, context: Context):
        return context.create_button(
            self._("list_create"),
            callback_data=self._get_create_command(context=context),
        )

    def _extra_buttons(self, context: Context):
        command_back = self._list_out(context=context)
        return [
            [self._create_button(context=context)],
            self._get_back_buttons(command_back=command_back, context=context),
        ]

    def command_navigate(self, context: Context):
        _, parameters = get_command_and_parameters(context.text)
        return self._list(page=parameters[0], context=context, update_last=True)

    command_navigate.use_history = True
