from collections import OrderedDict
from unittest.mock import patch

from tests import BaseTestClass
from tests.seed import seed_users

from src.services import AuthService


class TestAuthService(BaseTestClass):

    _access_token = 'eyJhbGciOiJIUzUxMiIl3LTRkNWYtNGJkYDRVRmaTh3ZI8F35qj6LWNA2c1Jx0uvr14o'
    _refresh_token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6he'

    @patch('src.services.auth_service.create_refresh_token')
    @patch('src.services.auth_service.create_access_token')
    def test_authorize_success(self,
                               create_access_token,
                               create_refresh_token):

        seed_users(self.db_connection)

        create_access_token.return_value = self._access_token
        create_refresh_token.return_value = self._refresh_token

        auth = AuthService.authorize(self.seed_payloads_password)

        self.assertIsInstance(auth, OrderedDict)
        self.assertEqual(dict(auth), self.response_access_user)

    def test_authorize_with_email_does_not_exists(self):
        seed_users(self.db_connection)

        data = self.seed_payloads_password
        data.update({
            'email': 'test@example.no'
            })

        auth = AuthService.authorize(data)
        self.assertEqual(auth, {})

    def test_authorize_with_password_fail(self):
        seed_users(self.db_connection)

        data = self.seed_payloads_password
        data.update({
            'password': '12345'
            })

        auth = AuthService.authorize(data)
        self.assertEqual(auth, {})

    def test_authorize_with_empty_data(self):
        seed_users(self.db_connection)

        data = self.seed_payloads_password
        data.update({
            'password': '12345'
            })

        auth = AuthService.authorize({})
        self.assertEqual(auth, {})

    @patch('src.services.auth_service.create_refresh_token')
    @patch('src.services.auth_service.create_access_token')
    def test_get_new_token_success(self,
                                   create_access_token,
                                   create_refresh_token):

        seed_users(self.db_connection)

        create_access_token.return_value = self._access_token
        create_refresh_token.return_value = self._refresh_token

        auth = AuthService.get_new_token('9bd82d2d-647f-4896-81ce-8055da610451')

        self.assertIsInstance(auth, OrderedDict)
        self.assertEqual(auth, self.response_access_user)

    def test_get_new_token_with_user_uuid_does_not_exists(self):
        seed_users(self.db_connection)

        auth = AuthService.get_new_token('c5244bd5-2d6b-474b-91e8-dfb6861e2b32')
        self.assertEqual(auth, {})

    def test_get_new_token_with_user_uuid_is_null(self):
        seed_users(self.db_connection)

        auth = AuthService.get_new_token(None)
        self.assertEqual(auth, {})

    def test_get_new_token_with_user_uuid_empty(self):
        seed_users(self.db_connection)

        auth = AuthService.get_new_token('')
        self.assertEqual(auth, {})
