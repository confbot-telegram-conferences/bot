import sys
import app.logging  # noqa
from app.config import Config
from app.injector import injector
from app.main import bot_manager, Main


def run_server():
    Main(injector).start()
    config = injector.get(Config)
    uri = f"{config.APP_HOST}/{config.TELEGRAM_TOKEN}"
    bot_manager(
        url=uri,
        polling=config.TELEGRAM_POLLING,
        token=config.TELEGRAM_TOKEN,
        port=config.APP_PORT,
    )


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("ERROR => You need to pass a command.")
    commands = {"run_server": run_server}
    commands[sys.argv[1]]()
