import re
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from imei_api.crud import user_crud
from imei_api.models import User


async def check_username_exists(
        session: AsyncSession, username) -> None or HTTPException:
    """Проверяет, существует ли пользователь с переданным именем в базе."""
    user = await user_crud.get_user_obj_by_name(session, username)
    if user is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Пользователь с таким username уже существует!',
        )


async def check_imei_correct(imei: str) -> str or HTTPException:
    """Убирает пробелы из imei и проверяет, что длина imei равна 15 цифрам."""
    imei: str = imei.replace(' ', '')
    if not re.fullmatch(r"\d{15}", imei):
        raise HTTPException(
            status_code=400,
            detail="IMEI должен содержать ровно 15 цифр"
        )
    return imei


async def check_token_exists(
        session: AsyncSession, token) -> None or HTTPException:
    """Проверяет, существует ли пользователь с переданным token в базе."""
    user: User = await user_crud.get_user_obj_by_token(session, token)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='token не найден. Получите token по /register',
        )
