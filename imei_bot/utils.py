import os
import re
from typing import Optional

import requests
from dotenv import load_dotenv
from requests import Response
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

load_dotenv()


def send_message(
        update: Update, context: CallbackContext, message: str) -> None:
    """Отправляет сообщение в Telegram чат."""
    chat = update.effective_chat
    context.bot.send_message(chat.id, message, )


def check_user_permission(
        update: Update, context: CallbackContext) -> Optional[bool]:
    """В зависимости от ответа API возвращает токен или информацию о
    регистрации."""
    token: Optional[bool] = check_user_in_whitelist(
        update.effective_chat.username)
    help_message: str = (
        'У вас нет доступа к боту. Чтобы получить доступ, '
        'пройдите регистрацию, указав свой телеграм username, на '
        '188.120.248.152/docs#/API/register_api_register_post')
    if token is None:
        send_message(update, context, message=help_message)
    else:
        return token


def check_user_in_whitelist(username: str) -> Optional[str]:
    """Возвращает токен пользователя, если пользователь есть в белом списке."""
    response: Response = requests.get(
        url=os.getenv('API_URL') + os.getenv('USER_CHECK_API_URL'),
        params={'tg_username': username}
    )
    if response.json().get('tg_username') == username:
        return response.json().get('token')
    return None


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


def check_imei_correct(imei: str) -> Optional[str]:
    """Убирает пробелы из imei и проверяет, что длина imei равна 15 цифрам."""
    imei: str = imei.replace(' ', '')
    if not re.fullmatch(r"\d{15}", imei):
        return None
    if not luhn_check(imei):
        return None
    return imei


def format_imei_info(data: dict) -> str:
    """Форматирует ответ API для вывода в Telegram автоматически."""
    if data.get('status') != 'successful':
        return 'Ошибка при проверке IMEI.'
    properties = data.get('properties', {})
    formatted_lines = [f'📱 Информация об устройстве\n']

    for key, value in properties.items():
        formatted_key = key.replace('_', ' ').capitalize()
        if isinstance(value, bool):
            value = 'Да' if value else 'Нет'
        formatted_lines.append(f'{formatted_key}: {value}')

    return '\n'.join(formatted_lines)


def chek_imei(imei: str, token: str) -> dict:
    """Делает запрос к API, возвращает информацию об IMEI."""
    response: Response = requests.post(
        url=os.getenv('API_URL') + os.getenv('IMEI_CHECK_API_URL'),
        params={'imei': imei, 'token': token}
    )
    return response.json()
