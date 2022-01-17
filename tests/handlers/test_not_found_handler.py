# from unittest.mock import patch
# from app.handlers.not_found_handler import NotFoundHandler


# def test_can_handler(injector, context):
#     assert not injector.get(NotFoundHandler).can_handler("some_test", context)


# def test_handle(injector, context):
#     with patch("app.core.Context.send_message") as mock_send_message:
#         injector.get(NotFoundHandler).handle(context)
#         mock_send_message.assert_called_once_with("no_found_text")
