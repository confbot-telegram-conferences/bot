from app.handlers2.error_handler import error_handler


def test_error_handler(translator, update, context):
    error_handler(update, context, translator)
    update.effective_message.reply_text.assert_called_with(
        " 😟 Ha ocurrido un error fatal. Vamos a solucionarlo pronto."
    )
