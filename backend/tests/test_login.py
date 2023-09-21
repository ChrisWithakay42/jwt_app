import pytest
from werkzeug.security import generate_password_hash

from backend.models import User


@pytest.mark.usefixtures('test_db')
class TestLogin:

    def test_login(self, test_client):
        password_hash = generate_password_hash('Admin12345!', method='sha256')
        user = User(
            user_name='TestUser',
            password_hash=password_hash
        )
        user.save()
        resp = test_client.post('/auth/login', json={'user_name': user.user_name, "password": 'Admin12345!'})
        assert resp.status_code == 200
