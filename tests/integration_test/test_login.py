from unittest.mock import patch

from tests import BaseTestClass
from tests.seed import seed_users

url = '/api/v1/login'
headers = {'Content-Type': 'application/json'}


class TestLogin(BaseTestClass):

    _access_token = 'eyJhbGciOiJIUzUxMiIl3LTRkNWYtNGJkYDRVRmaTh3ZI8F35qj6LWNA2c1Jx0uvr14o'
    _refresh_token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6he'

    @patch('src.services.auth_service.create_refresh_token')
    @patch('src.services.auth_service.create_access_token')
    def test_login_success(self,
                           create_access_token,
                           create_refresh_token):

        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        create_access_token.return_value = self._access_token
        create_refresh_token.return_value = self._refresh_token

        response = self.api.post(url,  headers=headers, json=self.seed_payloads_password)
        self.assert_json_response(response, 'Successful request', 200, self.response_access_user)

    def test_login_email_format_fail(self):

        seed_users(self.db_connection)

        credentials = self.seed_payloads_password
        credentials.update({
            'email': '2test123l'
            })

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        expected_exceptions = {
            'email': ['Not a valid email address.']
            }

        response = self.api.post(url,  headers=headers, json=self.seed_payloads_password)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_login_email_fail(self):

        seed_users(self.db_connection)

        credentials = self.seed_payloads_password
        credentials.update({
            'email': 'testno@email.com'
            })

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        expected_exceptions = {
            'Login': 'Error in password or email.'
            }

        response = self.api.post(url,  headers=headers, json=self.seed_payloads_password)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_login_password_fail(self):

        seed_users(self.db_connection)

        credentials = self.seed_payloads_password
        credentials.update({
            'password': 'test_password'
            })

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        expected_exceptions = {
            'Login': 'Error in password or email.'
            }

        response = self.api.post(url,  headers=headers, json=self.seed_payloads_password)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_login_empty_credentials(self):

        seed_users(self.db_connection)

        credentials = {
            'email': '',
            'password': ''
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        expected_exceptions = {
            'email': ['Not a valid email address.',
                      'Length must be between 8 and 70.']
            }

        response = self.api.post(url,  headers=headers, json=credentials)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_login_without_email(self):

        seed_users(self.db_connection)

        credentials = self.seed_payloads_password
        credentials.pop('email')

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        expected_exceptions = {
            'email': ['Missing data for required field.']
            }

        response = self.api.post(url,  headers=headers, json=self.seed_payloads_password)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_login_without_password(self):

        seed_users(self.db_connection)

        credentials = self.seed_payloads_password
        credentials.pop('password')

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        expected_exceptions = {
            'password': ['Missing data for required field.']
            }

        response = self.api.post(url,  headers=headers, json=self.seed_payloads_password)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_login_without_authorized(self):
        headers.pop('Authorization')

        response = self.api.post(url, headers=headers, json=self.seed_payloads_new_user)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_login_with_authorized_bad_token(self):
        headers.update({
            'Authorization': 'Basic HVXLzhVdz09OjUreS9CeVBwc3BFaUVrR3Y3VnF2RGsrVS9ZW'
            })

        response = self.api.post(url, headers=headers, json=self.seed_payloads_new_user)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_login_without_header_json(self):
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': f'Basic {self.credentials}'}

        response = self.api.post(url, headers=headers, json=self.seed_payloads_new_user)
        self.assert_json_response(response, 'Bad Request', 400, None)
