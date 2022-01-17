# from tests.factories import message_context
# from unittest.mock import patch
# from app.handlers.start_handler import StartHandler


# def test_can_handler(injector, context):
#     assert injector.get(StartHandler).can_handler("/start", context)


# def test_handle(injector, context):
#     context.message = message_context(text="/start")
#     context.user.handler_data = {"other_data": "any_data"}
#     context.user.step = "some_text"
#     context.user.current_handler = (
#         "<class 'app.handlers.book_fair_handler.BookFairHandler'>"
#     )
#     handler = injector.get(StartHandler)
#     with patch("app.core.Context.send_message") as mock_send_message:
#         handler.handle(context)
#         assert not context.user.current_handler
#         assert not context.user.step
#         assert context.user.handler_data == {}
#         mock_send_message.assert_called_once_with("start_bot_reseted")
