from uuid import uuid4

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from api.schemas import UserRegister, UserDB
from core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.description
)

USERS = {}


@app.post('/register', response_model=UserDB)
async def register(user: UserRegister):
    if user.username in USERS:
        raise HTTPException(status_code=400,
                            detail='Пользователь уже зарегистрирован')
    token = str(uuid4())
    USERS[user.username] = token
    return {"username": user.username, "token": token}


@app.get('/')
def read_root() -> RedirectResponse:
    return RedirectResponse(url='/docs')


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
