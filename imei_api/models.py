from sqlalchemy import Column, String

from imei_api.core.db import Base


class User(Base):
    """Модель пользователя."""
    username = Column(String(100), unique=True, nullable=False)
    token = Column(String(100), unique=True, nullable=False)
    tg_username = Column(String(100), unique=True)
