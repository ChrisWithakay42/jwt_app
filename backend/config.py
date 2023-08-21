from pydantic.v1 import BaseSettings


class AppConfig(BaseSettings):
    FLASK_APP: str = 'autoapp.py'
    LOG_LEVEL: str = 'INFO'
    DEBUG: bool = False
