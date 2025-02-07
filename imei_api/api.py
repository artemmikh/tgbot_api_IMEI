import json
from uuid import uuid4

import requests
from fastapi import Depends, Query, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from imei_api.core.config import settings
from imei_api.core.db import get_async_session
from imei_api.crud import user_crud
from imei_api.models import User
from imei_api.schemas import UserRegister, UserDB
from imei_api.validators import check_username_exists, check_imei_correct, \
    check_token_exists, check_tg_username_exists, check_username_not_exists, \
    check_tg_username_not_exists

router = APIRouter()


@router.post(
    '/register',
    response_model=UserDB,
    response_model_exclude_none=True,
)
async def register(
        user: UserRegister,
        session: AsyncSession = Depends(get_async_session)
) -> UserDB or HTTPException:
    """Регистрирует пользователя, присваивая токен."""
    await check_username_not_exists(session, user.username)
    if user.tg_username is not None:
        await check_tg_username_not_exists(session, user.tg_username)
    token = str(uuid4())
    user_data: dict = {
        'username': user.username,
        'token': token,
        'tg_username': user.tg_username
    }
    new_user: User = await user_crud.create(user_data, session)

    return UserDB(
        username=new_user.username,
        token=new_user.token,
        tg_username=user.tg_username
    )


@router.post('/register/add_tg_username')
async def add_tg_username_to_user(
        username: str = Query(
            ..., description='Имя зарегистрированного пользователя'),
        tg_username: str = Query(..., description='Телеграм username'),
        session: AsyncSession = Depends(get_async_session)
):
    """Добавляет телеграм username для зарегистрированного пользователя."""
    user = await check_username_exists(session, username)
    await check_tg_username_not_exists(session, tg_username)
    user_data: dict = {'tg_username': tg_username}
    return await user_crud.update(user, user_data, session)


@router.post('/check_imei')
async def check_imei(
        imei: str = Query(..., description="IMEI устройства"),
        token: str = Query(..., description="Токен авторизации "
                                            "(получить токен можно по запросу "
                                            "на /register)"),
        session: AsyncSession = Depends(get_async_session)
):
    """Проверяет валидность imei и token, получает инфо об imei с внешнего
    API."""
    await check_token_exists(session, token)
    imei = await check_imei_correct(imei)

    payload = json.dumps({
        "deviceId": imei,
        "serviceId": settings.imei_check_service_id
    })
    token_mode = settings.token_api_sandbox if settings.sandbox_mode else (
        settings.token_api_live)
    headers = {
        'Authorization': f'Bearer {token_mode}',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST",
        url=settings.imei_check_url,
        headers=headers, data=payload)
    return response.json()


@router.get('/register')
async def get_user_by_tg_username(
        tg_username: str = Query(..., description='Телеграм username'),
        session: AsyncSession = Depends(get_async_session)
):
    """Возвращает данные о пользователе по token."""
    user = await check_tg_username_exists(session, tg_username)
    return UserDB(
        username=user.username,
        tg_username=user.tg_username,
        token=user.token
    )
