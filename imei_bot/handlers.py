from imei_bot.utils import send_message, check_user_in_whitelist


def start_handler(update, context):
    """Обработчик команды /start. Проверяет, есть ли пользователь в
    белом списке. В зависимости от этого отправляет нужное сообщение с
    информацией."""
    user: bool = check_user_in_whitelist(update.effective_chat.username)
    help_message = (
        'У вас нет доступа к боту. Чтобы получить доступ, '
        'пройдите регистрацию, указав свой телеграм username, на '
        'http://127.0.0.1:8000/docs#/API/register_api_register_post')
    send_message(
        update,
        context,
        message='Добро пожаловать!' if user else help_message)
