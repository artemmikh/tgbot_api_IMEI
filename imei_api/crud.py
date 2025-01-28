from typing import Optional, Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from imei_api.models import User


class CRUDUser:

    def __init__(self, model):
        """Инициализация CRUD с указанной моделью."""
        self.model = model

    async def create(self, obj_in: Dict, session: AsyncSession) -> User:
        """Создать новый объект."""
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_user_obj_by_name(
            self, session: AsyncSession, username: str) -> Optional[User]:
        """Получить объект пользователя по имени."""
        user = await session.execute(
            select(User).where(User.username == username)
        )
        return user.scalars().first()

    async def get_user_obj_by_token(
            self, session: AsyncSession, token: str) -> Optional[User]:
        """Получить объект пользователя по токену."""
        user = await session.execute(
            select(User).where(User.token == token)
        )
        return user.scalars().first()


user_crud = CRUDUser(User)
