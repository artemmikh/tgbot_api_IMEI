import os

import requests

from dotenv import load_dotenv
from requests import Response

load_dotenv()


def send_message(update, context, message):
    """Отправляет сообщение в Telegram чат."""
    chat = update.effective_chat
    context.bot.send_message(chat.id, message)


def check_user_in_whitelist(username: str) -> bool:
    """Делает запрос к API, возвращает True/False в зависимости от ответа."""
    response: Response = requests.get(
        url=os.getenv('IMEI_CHECK_API_URL'),
        params={'tg_username': username}
    )
    if response.json().get('tg_username') == username:
        return True
    else:
        return False
