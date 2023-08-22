import base64
import json
import datetime

import pytest

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

    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=180)
    token = {
        'user_uuid': 'fake uuid4',
        'exp': expiration_time.timestamp()
    }
    auth_header = b'Basic ' + base64.b64encode(json.dumps(token).encode())
    testing_client.environ_base['HTTP_X_ACCESS_TOKEN'] = auth_header

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
