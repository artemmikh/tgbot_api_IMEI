import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from imei_api.api import router as api_router
from imei_api.core.config import settings
from imei_api.core.db import engine, Base
from imei_api.models import User  # noqa

main_router = APIRouter()
main_router.include_router(
    api_router,
    prefix='/api',
    tags=['API'],
)
app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)

app.include_router(main_router)


@app.on_event("startup")
async def on_startup():
    """Создание таблиц при старте приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/')
def redirect_to_swagger() -> RedirectResponse:
    """Перенаправляет с главной на документацию."""
    return RedirectResponse(url='/docs')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
