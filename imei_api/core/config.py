from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""
    app_title: str = 'API IMEI'
    description: str = 'API для проверки IMEI устройств'
    database_url: str = 'sqlite+aiosqlite:///./IMEI.db'

    class Config:
        env_file: str = '.env'


settings = Settings()
