from app.core.callback_context import CallbackContext
from functools import reduce
from queue import Queue
from injector import Injector, inject, singleton
from telegram import Update, Bot
from telegram.ext import Dispatcher as BaseDispatcher, ContextTypes, JobQueue
from app.config import Config
from app.core.my_persisiter import MyPersister
from app.models.repositories.user_repository import TELEGRAM_ID_FIELD, UserRepository


@singleton
class Dispatcher(BaseDispatcher):
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
        config: Config,
        injector: Injector,
        bot: Bot,
        persistence: MyPersister,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            bot=bot,
            persistence=persistence,
            update_queue=Queue(),
            job_queue=JobQueue(),
            workers=4,
            context_types=ContextTypes(context=CallbackContext),
            **kwargs,
        )
        self.user_repository = user_repository
        self.config = config
        self.injector = injector
        self._group_commands = []
        self._private_commands = []
        self._user = None

    @property
    def user(self):
        return self._user

    @property
    def group_commands(self):
        return self._group_commands

    @property
    def group_commands_private(self):
        return self._private_commands

    @property
    def group_commands_clean(self):
        return [command for command, _ in self.group_commands]

    def process_update(self, update: Update, *args, **kwargs) -> None:
        user = update.effective_user
        if user:
            first_name = (
                getattr(user, "first_name") if getattr(user, "first_name") else ""
            )
            last_name = getattr(user, "last_name") if getattr(user, "last_name") else ""
            data = {
                TELEGRAM_ID_FIELD: getattr(user, "id"),
                "first_name": first_name[0:29],
                "last_name": last_name[0:29],
                "language_code": getattr(user, "language_code"),
                "is_bot": getattr(user, "is_bot"),
            }
            update.model_user = self.user_repository.get_or_create_user(
                user.id, {TELEGRAM_ID_FIELD: user.id}, data
            )
            self._user = update.model_user
        return super().process_update(update, *args, **kwargs)

    def get_my_commands(self):
        commands = [
            self.injector.get(handler_class).get_start_commands_with_description()
            for handler_class in self.config.handlers
        ]
        return reduce(lambda a, c: a + c, commands, [])
