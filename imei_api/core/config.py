from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""
    app_title: str = 'API IMEI'
    description: str = 'API для проверки IMEI устройств'
    database_url: str = 'sqlite+aiosqlite:///./IMEI.db'
    imei_check_url: str = 'https://api.imeicheck.net/v1/checks'
    token_api_live: str = 'example'
    token_api_sandbox: str = 'example'
    imei_check_service_id: int = 12

    class Config:
        env_file: str = '.env'


settings = Settings()
