# from app.handlers.help_handler import HelpHandler


# def test_can_handler(injector, context):
#     assert injector.get(HelpHandler).can_handler("/help", context)


# def test_cant_handler(injector, context):
#     assert not injector.get(HelpHandler).can_handler("other_text", context)


# # def test_handle(injector, context):
# #     context.message = message_context(text="/help")
# #     with patch("app.core.Context.send_message") as mock_send_message:
# #         injector.get(HelpHandler).handle(context)
# #         mock_send_message.assert_called_once_with(
# #             use_history=False, message="It is the help of the bot"
# #         )
