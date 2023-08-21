import pytest

from backend.models import User


@pytest.mark.usefixtures('test_db')
class TestCreateUser:
    data = {
        'name': 'admin',
        'password': '12345'
    }
    api_url = '/app/users'

    def test_create_new_user(self, test_client):
        resp = test_client.post(self.api_url, json=self.data)
        assert resp.status_code == 200
        assert resp.json['data'] == 'New user created.'
        users = User.query.all()
        assert len(users) == 1

    def test_list_users(self, test_client):
        resp = test_client.get(self.api_url)
        assert resp.status_code == 200
