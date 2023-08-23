import pytest

from backend.models import User


@pytest.mark.usefixtures('test_db')
class TestLogin:

    def test_login(self, test_client):
        user = User(
            name='TestUser',
            password_hash='12345'
        )
        user.save()
        resp = test_client.get('/login', json={'user_name': user.user_name, "password": '12345'})
        assert resp.status_code == 200
