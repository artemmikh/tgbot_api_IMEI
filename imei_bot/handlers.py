from telegram import Update
from telegram.ext import CallbackContext

from imei_bot.utils import send_message, check_imei_correct, chek_imei, \
    check_user_permission, format_imei_info


def start_handler(update: Update, context: CallbackContext) -> None:
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


def message_handler(update: Update, context: CallbackContext) -> None:
    """Обработчик входящих сообщений."""
    token: str or None = check_user_permission(update, context)
    if token is None:
        return
    imei: str = update.effective_message.text
    imei_correct: str or None = check_imei_correct(imei)
    if imei_correct is None:
        message: str = 'Проверьте корректность IMEI.'
        send_message(update, context, message)
    else:
        imei_info: str = chek_imei(imei_correct, token)
        imei_info: str = format_imei_info(imei_info)
        send_message(update, context, imei_info)
