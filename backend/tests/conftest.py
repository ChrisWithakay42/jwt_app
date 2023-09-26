import base64
import json
import datetime
from uuid import uuid4

import jwt
import pytest
from werkzeug.security import generate_password_hash

from backend.app import create_app
from backend.app import get_config_object
from backend.extensions import db
from backend.models import User


@pytest.fixture(scope='session')
def test_app():
    app = create_app(config_object=get_config_object())
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def test_db(test_app):
    """A database for the tests."""
    db.app = test_app
    with test_app.app_context():
        db.create_all()

    yield db

    # Explicitly close DB connection
    db.session.close()
    db.drop_all()


@pytest.fixture(scope='module')
def test_client(test_app):
    testing_client = test_app.test_client()

    user_uuid = str(uuid4())
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=180)

    secret_key = test_app.config['SECRET_KEY']
    token_payload = {
        'user_uuid': user_uuid,
        'exp': expiration_time,
    }
    token = jwt.encode(token_payload, secret_key, algorithm='HS256')

    testing_client.environ_base['HTTP_X_ACCESS_TOKEN'] = f'Bearer {token}'
    yield testing_client


@pytest.fixture
def user_factory():
    users = []
    for i in range(3):
        user = User(
            name=f'name_{i}',
            password_hash=f'12345{i}'
        )
        user.save()
        users.append(user)
    return users


@pytest.fixture
def user():
    password_hash = generate_password_hash('Admin12345!', method='sha256')
    user = User(
        user_name='TestUser',
        password_hash=password_hash
    )
    user.save()
    return user
