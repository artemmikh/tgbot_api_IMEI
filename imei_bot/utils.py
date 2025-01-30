import os
import re

import requests
from dotenv import load_dotenv
from requests import Response

load_dotenv()


def send_message(update, context, message):
    """Отправляет сообщение в Telegram чат."""
    chat = update.effective_chat
    context.bot.send_message(chat.id, message)


def check_user_permission(update, context):
    token: bool = check_user_in_whitelist(update.effective_chat.username)
    help_message: str = (
        'У вас нет доступа к боту. Чтобы получить доступ, '
        'пройдите регистрацию, указав свой телеграм username, на '
        'http://127.0.0.1:8000/docs#/API/register_api_register_post')
    if token is None:
        send_message(update, context, message=help_message)
    else:
        return token


def check_user_in_whitelist(username: str) -> str:
    """Возвращает токен пользователя, если пользователь есть в белом списке."""
    response: Response = requests.get(
        url=os.getenv('API_URL') + os.getenv('USER_CHECK_API_URL'),
        params={'tg_username': username}
    )
    if response.json().get('tg_username') == username:
        return response.json().get('token')


def luhn_check(imei: str) -> bool:
    """Проверяет IMEI с использованием алгоритма Luhn."""
    digits = [int(d) for d in imei]
    checksum = 0

    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return checksum % 10 == 0


def check_imei_correct(imei: str) -> str:
    """Убирает пробелы из imei и проверяет, что длина imei равна 15 цифрам."""
    imei: str = imei.replace(' ', '')
    if not re.fullmatch(r"\d{15}", imei):
        return
    if not luhn_check(imei):
        return
    return imei


def chek_imei(imei, token):
    """Делает запрос к API, возвращает информацию об IMEI."""
    response: Response = requests.post(
        url=os.getenv('API_URL') + os.getenv('IMEI_CHECK_API_URL'),
        params={'imei': imei, 'token': token}
    )
    return response.json()
