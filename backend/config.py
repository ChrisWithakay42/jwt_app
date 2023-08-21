import os

from pydantic.v1 import BaseSettings

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


class AppConfig(BaseSettings):
    FLASK_APP: str = 'autoapp.py'
    LOG_LEVEL: str = 'INFO'
    DEBUG: bool = False
    SECRET_KEY: str = 'not-so-secret-while-in-development'

    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_ECHO: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'connect_args': {
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5
        }
    }

    class Config:
        env_file = PROJECT_ROOT + '/backend/.env'
        env_file_encoding = 'utf-8'
        fields = {
            'SQLALCHEMY_DATABASE_URI': {
                'env': 'DATABASE_URL'
            }
        }


