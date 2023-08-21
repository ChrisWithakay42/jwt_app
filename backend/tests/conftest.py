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
    yield testing_client


@pytest.fixture
def user_factory():
    for _ in range(3):
        user = User(
            name='name',
            password=''
        )
        user.save()
