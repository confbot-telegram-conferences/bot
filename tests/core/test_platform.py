# from unittest.mock import patch, MagicMock
# from app.core.exception import HandlerNotFoundException, Context
# from app.handlers import HelpHandler
# from app.injector import injector


# class Config:
#     def __init__(self, handlers):
#         self.handlers = handlers


# @patch.multiple(Context, __abstractmethods__=set())
# @patch("app.handlers.HelpHandler.can_handler", return_value=True)
# def test_get_handler(*args, **kwargs):
#     config = Config([HelpHandler])
#     context = Context(injector, config, MagicMock())
#     handler = context.get_handler()
#     assert isinstance(handler, HelpHandler)


# @patch.multiple(Context, __abstractmethods__=set())
# @patch("app.handlers.HelpHandler.can_handler", return_value=False)
# def test_not_get_handler(*args, **kwargs):
#     config = Config([HelpHandler])
#     context = Context(injector, config, MagicMock())
#     try:
#         context.get_handler()
#         assert False
#     except HandlerNotFoundException:
#         assert True


# @patch.multiple(Context, __abstractmethods__=set())
# @patch("app.handlers.HelpHandler.handle", return_value="test_to_send")
# @patch("app.core.Context.send_message")
# def test_handle(*args, **kwargs):
#     help_handler = injector.get(HelpHandler)
#     context = MagicMock()
#     with patch("app.core.Context.get_handler", return_value=help_handler):
#         config = Config([HelpHandler])
#         context = Context(injector, config, MagicMock())
#         context()
#         HelpHandler.handle.assert_called_once()
#         context.user_repository.update.assert_called_once()


# @patch.multiple(Context, __abstractmethods__=set())
# def test_send_one_message():
#     with patch("app.core.Context._send_message") as mock_send_message, patch(
#         "app.core.Context.get_user", return_value=MagicMock()
#     ):
#         context = Context(injector, MagicMock(), MagicMock())
#         context.send_message("one_text")
#         mock_send_message.assert_called_once_with("one_text")


# @patch.multiple(Context, __abstractmethods__=set())
# def test_send_multiple_message():
#     with patch("app.core.Context._send_message") as mock_send_message, patch(
#         "app.core.Context.get_user", return_value=MagicMock()
#     ):
#         context = Context(injector, MagicMock(), MagicMock())
#         context.send_messages(["one_text", "other_text"])
#         first, secound = mock_send_message.mock_calls
#         assert first[1][0] == "one_text"
#         assert secound[1][0] == "other_text"
