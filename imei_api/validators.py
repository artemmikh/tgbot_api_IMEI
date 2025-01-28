import re
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from imei_api.crud import user_crud


async def check_username_exists(session: AsyncSession, username):
    """Проверяет, существует ли пользователь с переданным именем в базе."""
    user = await user_crud.get_user_by_name(session, username)
    if user is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Пользователь с таким username уже существует!',
        )


async def check_imei_correct(imei: str):
    """Убирает пробелы из imei и проверяет, что длина imei равна 15 цифрам."""
    imei = imei.replace(' ', '')
    if not re.fullmatch(r"\d{15}", imei):
        raise HTTPException(
            status_code=400,
            detail="IMEI должен содержать ровно 15 цифр"
        )
    return imei


async def check_token_exists(session: AsyncSession, token):
    """Проверяет, существует ли пользователь с переданным token в базе."""
    user = await user_crud.get_user_by_token(session, token)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='token не найден. Получите token по /register',
        )
