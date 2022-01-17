from app.services.api.entities.conference import Conference
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context


class NameMixin:
    def command_change_name(self, context: Context, service: ConferenceAdminApiService):
        context.user.step = "wait_change_name"
        buttons = [
            [
                self.create_back_button(context=context),
            ]
        ]
        conference_id = context.user.handler_data["conference_id"]
        conference: Conference = service.get_by_id(conference_id, user=context.user)
        header = self._get_header_text(conference=conference, context=context)
        return context.build_buttons(
            buttons, message=header + self._("conference_create_change_name")
        )

    command_change_name.use_history = True

    def wait_change_name(self, context: Context, service: ConferenceAdminApiService):
        conference_id = context.user.handler_data["conference_id"]
        if context.text:
            conference: Conference = service.get_by_id(conference_id, user=context.user)
            conference.name = context.text
            service.update(conference, user=context.user)
        return context.forward(f"/init_conference {conference_id}")

    wait_change_name.clear_history = True
