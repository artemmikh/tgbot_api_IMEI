from imei_bot.utils import send_message, check_imei_correct, chek_imei, \
    check_user_permission


def start_handler(update, context):
    """Обработчик команды /start. Проверяет, есть ли пользователь в
    белом списке. В зависимости от этого отправляет нужное сообщение с
    информацией."""
    token: bool = check_user_permission(update, context)
    if token is not None:
        send_message(
            update,
            context,
            message='Добро пожаловать! Отправьте в чат IMEI для проверки'
        )


def message_handler(update, context):
    token: str or None = check_user_permission(update, context)
    if token is None:
        return
    imei = check_imei_correct(update.effective_message.text)
    if imei is None:
        message = ('Проверьте корректность IMEI. '
                   'IMEI должен содержать ровно 15 цифр')
        send_message(update, context, message)
    else:
        imei_info = chek_imei(imei, token)
        send_message(update, context, imei_info)
