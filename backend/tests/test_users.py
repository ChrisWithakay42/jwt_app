import pytest

from backend.models import User


@pytest.mark.usefixtures('test_db')
class TestUserEndpoint:
    data = {
        'user_name': 'admin',
        'password': '12345'
    }
    api_url = '/frontend/users'

    def test_create_new_user(self, test_client):
        resp = test_client.post(self.api_url, json=self.data)
        assert resp.status_code == 200
        assert resp.json['data'] == 'New user created.'
        users = User.query.all()
        assert len(users) == 1

    def test_list_users(self, test_client, user_factory):
        resp = test_client.get(self.api_url)
        assert resp.status_code == 200
        users = User.query.all()
        assert len(users) == 3

    def test_get_one_user(self, test_client, user_factory):
        user = user_factory[0]
        resp = test_client.get(f'{self.api_url}/{user.user_uuid}')
        assert resp.status_code == 200

    def test_promote_user(self, test_client, user_factory):
        user = user_factory[0]
        resp = test_client.put(f'{self.api_url}/{user.user_uuid}')
        assert resp.status_code == 200
        assert user.is_admin is True

    def test_delete_user(self, test_client, user_factory):
        user = user_factory[0]
        resp = test_client.delete(f'{self.api_url}/{user.user_uuid}')
        assert resp.status_code == 200
        assert resp.json['data'] == 'User has been deleted.'


