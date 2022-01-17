from app.services.api.entities.group_channel import GroupChannel
from app.services.api.group_channel_admin import GroupChannelAdminApiService
from app.config import Config
from app.core.context import Context
from app.core.handler import Handler


class NewMembersHandler(Handler):
    def get_start_commands(self):
        return ["/new_members"]

    def is_group_handler(self, context: Context):
        return True

    def start(
        self,
        context: Context,
        config: Config,
        group_channel_service: GroupChannelAdminApiService,
    ):
        message = context.input["message"]
        new_members = [item["username"] for item in message["new_chat_members"]]
        if config.TELEGRAM_BOT_NAME not in new_members:
            return
        entity: GroupChannel = group_channel_service.create_entity(
            external_id=message["chat"]["id"],
            title=message["chat"]["title"],
            type=message["chat"]["type"],
            data=context.input,
        )
        group_channel_service.save(entity, user=context.user)
        return self._("new_members")
