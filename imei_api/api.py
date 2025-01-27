from uuid import uuid4

from fastapi import Depends, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from imei_api.core.db import get_async_session
from imei_api.crud import user_crud
from imei_api.models import User  # noqa
from imei_api.schemas import UserRegister, UserDB
from imei_api.validators import check_username_exists, check_imei_correct, \
    check_token_exists

router = APIRouter()


@router.post('/register', response_model=UserDB)
async def register(
        user: UserRegister,
        session: AsyncSession = Depends(get_async_session)):
    await check_username_exists(session, user.username)
    token = str(uuid4())
    user_data = {"username": user.username, "token": token}
    new_user = await user_crud.create(user_data, session)

    return UserDB(username=new_user.username, token=new_user.token)


@router.post('/check_imei')
async def check_imei(
        imei: str = Query(..., description="IMEI устройства"),
        token: str = Query(..., description="Токен авторизации "
                                            "(получить токен можно по запросу "
                                            "на /register)"),
        session: AsyncSession = Depends(get_async_session)
):
    await check_token_exists(session, token)
    imei = await check_imei_correct(imei)
