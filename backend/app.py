from flask import Flask

from backend.api.users import users
from backend.auth.login import login_bp
from backend.config import AppConfig
from backend.extensions import cors
from backend.extensions import db
from backend.extensions import migrate


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
    migrate.init_app(app, db)
    cors(app)


def register_blueprints(app: Flask):
    app.register_blueprint(users.users_api)
    app.register_blueprint(login_bp)
