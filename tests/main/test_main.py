# from unittest.mock import MagicMock
# from app.injector import injector
# from app.core.config import Config
# from app.main import Main
# from app.telegram import TelegramStarter


# def test_load_handlers():
#     config: Config = injector.get(Config)
#     assert len(config.handlers) == 8  # The total of handlers registered


# def test_start():
#     start_mock = MagicMock()
#     TelegramStarter.__call__ = start_mock
#     main = Main(injector)
#     main.start([TelegramStarter])
#     start_mock.assert_called_once()
