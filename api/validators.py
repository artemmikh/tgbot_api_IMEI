from http import HTTPStatus

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
