from http import HTTPStatus
import re

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import user_crud


async def check_username_exists(session: AsyncSession, username):
    """Проверяет, существует ли пользователь с переданным именем в базе."""
    user = await user_crud.get_user_by_name(session, username)
    if user is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Пользователь с таким username уже существует!',
        )


async def check_imei_correct(imei: str):
    imei = imei.replace(' ', '')
    if not re.fullmatch(r"\d{15}", imei):
        raise HTTPException(
            status_code=400,
            detail="IMEI должен содержать ровно 15 цифр"
        )
    return imei


async def check_token_exists(session: AsyncSession, token):
    user = await user_crud.get_user_by_token(session, token)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='token не найден. Получите token по /register',
        )
