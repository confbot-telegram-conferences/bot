from app.services.api.entities.conference import Conference
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context


class ActiveMixin:
    def command_active_conference(
        self, context: Context, service: ConferenceAdminApiService
    ):
        conference_id = context.user.handler_data["conference_id"]
        conference: Conference = service.get_by_id(conference_id, user=context.user)
        active_desactive_lb = (
            self._("conference_desactive_btn")
            if conference.active
            else self._("conference_active_btn")
        )
        buttons = [
            [
                context.create_button(
                    active_desactive_lb, callback_data="/do_active_conference"
                ),
                self.create_back_button(context=context),
            ]
        ]
        header = self._get_header_text(conference=conference, context=context)
        return context.build_buttons(
            buttons,
            message=header + self._("conference_active_lb"),
        )

    command_active_conference.use_history = True

    def command_do_active_conference(
        self, context: Context, service: ConferenceAdminApiService
    ):
        conference_id = context.user.handler_data["conference_id"]
        conference: Conference = service.get_by_id(conference_id, user=context.user)
        conference.active = not conference.active
        service.update(conference, user=context.user)
        return context.forward(f"/conference {conference_id}")

    command_do_active_conference.use_history = True
