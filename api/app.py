import asyncio
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import settings
from api.core.db import engine, Base, get_async_session
from api.crud import user_crud
from api.models import User  # noqa
from api.schemas import UserRegister, UserDB
from api.validators import check_username_exists, check_imei_correct, \
    check_token_exists

app = FastAPI(
    title=settings.app_title,
    description=settings.description
)


@app.post('/register', response_model=UserDB)
async def register(
        user: UserRegister,
        session: AsyncSession = Depends(get_async_session)):
    await check_username_exists(session, user.username)
    token = str(uuid4())
    user_data = {"username": user.username, "token": token}
    new_user = await user_crud.create(user_data, session)

    return UserDB(username=new_user.username, token=new_user.token)


@app.get('/')
def read_root() -> RedirectResponse:
    return RedirectResponse(url='/docs')


@app.get('/imei')
async def check_imei(
        imei: str = Query(..., description="IMEI устройства"),
        token: str = Query(..., description="Токен авторизации "
                                            "(получить токен можно по запросу "
                                            "на /register)"),
        session: AsyncSession = Depends(get_async_session)
):
    await check_token_exists(session, token)
    imei = await check_imei_correct(imei)


async def create_tables() -> None:
    """Создает таблицы в базе данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())
    uvicorn.run('app:app', reload=True)
