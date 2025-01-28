import requests


def send_message(update, context, message):
    """Отправляет сообщение в Telegram чат."""
    chat = update.effective_chat
    context.bot.send_message(chat.id, message)


def check_user_in_whitelist(username):
    return False
