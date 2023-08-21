from flask import Flask

from backend.api.users import users
from config import AppConfig
from extensions import db


def get_config_object():
    config_instance = AppConfig()
    return config_instance


def create_app(config_object: AppConfig = None):
    if config_object is None:
        config_object = get_config_object()

    app = Flask(__name__)

    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)


def register_blueprints(app: Flask):
    app.register_blueprint(users)
