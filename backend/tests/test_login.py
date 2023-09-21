import pytest
from werkzeug.security import generate_password_hash

from backend.models import User


@pytest.fixture
def login_data():
    return {
        'user_name': 'TestUser',
        'password': 'Admin12345!'
    }


@pytest.mark.usefixtures('test_db')
class TestLogin:
    base_url = '/auth/login'

    def test_login_success(self, test_client, user):
        resp = test_client.post(self.base_url, json={'user_name': user.user_name, "password": 'Admin12345!'})
        assert resp.status_code == 200

        assert 'Bearer' in resp.json['token']

    @pytest.mark.parametrize('field', ['user_name', 'password'])
    def test_when_missing_credentials(self, test_client, field, user, login_data):
        del login_data[field]
        resp = test_client.post(self.base_url, json=login_data)
        assert resp.status_code == 400
        assert resp.json == {'message': 'Missing username or password'}

    def test_user_does_not_exist(self, test_client, login_data):
        resp = test_client.post(self.base_url, json=login_data)
        assert resp.status_code == 401
        assert resp.json == {'message': 'Could not verify User.'}

    def test_wrong_password(self, test_client, login_data, user):
        login_data['password'] = 'wrong_password'
        resp = test_client.post(self.base_url, json=login_data)
        assert resp.status_code == 401
        assert resp.json == {'message': 'Could not verify Password.'}
