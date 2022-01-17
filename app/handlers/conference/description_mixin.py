from app.services.api.entities.conference import Conference
from app.services.api.conference_admin import ConferenceAdminApiService
from app.core.context import Context


class DescriptionMixin:
    def command_change_description(
        self, context: Context, service: ConferenceAdminApiService
    ):
        context.user.step = "wait_change_description"
        conference_id = context.user.handler_data["conference_id"]
        conference: Conference = service.get_by_id(conference_id, user=context.user)
        buttons = [
            [
                self.create_back_button(context=context),
            ]
        ]
        header = self._get_header_text(conference=conference, context=context)
        return context.build_buttons(
            buttons, message=header + self._("conference_create_change_description")
        )

    command_change_description.use_history = True

    def wait_change_description(
        self, context: Context, service: ConferenceAdminApiService
    ):
        conference_id = context.user.handler_data["conference_id"]
        if context.text:
            conference: Conference = service.get_by_id(conference_id, user=context.user)
            conference.description = context.text
            service.update(conference, user=context.user)
        return context.forward(f"/init_conference {conference_id}")

    wait_change_description.clear_history = True
