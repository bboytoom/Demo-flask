from flask_jwt_extended import create_access_token

from tests import BaseTestClass
from tests.seed import seed_users

url = '/api/v1/users/'
headers = {'Content-Type': 'application/json'}
USER_UUID = '9bd82d2d-647f-4896-81ce-8055da610451'


class TestUpdatePassword(BaseTestClass):

    def test_update_password_success(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': data.get('password')
            })

        response = self.api.patch(url + USER_UUID + '/change-password', headers=headers, json=data)
        self.assert_json_response(response, 'Successful request', 200, None)

    def test_update_password_fail_password_confirmed(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': 'test1234@P'
            })

        expected_exceptions = {
            'password_confirmed': ['Passwords must match.']
            }

        response = self.api.patch(url + USER_UUID + '/change-password', headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_password_without_password_confirmed(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('email')

        expected_exceptions = {
            'password_confirmed': ['Missing data for required field.']
            }

        response = self.api.patch(url + USER_UUID + '/change-password', headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_password_with_password_confirmed_min(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': 'a'
            })

        expected_exceptions = {
            'password_confirmed': ['Length must be between 8 and 30.']
            }

        response = self.api.patch(url + USER_UUID + '/change-password', headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_password_with_password_confirmed_invalid(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': 'aaaaaaaa'
            })

        expected_exceptions = {
            'password_confirmed': [
                'The password must have at least one capital letter.',
                'The password must have at least one number.',
                'The password must have at least one special character.']
            }

        response = self.api.patch(url + USER_UUID + '/change-password', headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_password_fail_passwords(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = {
            'password': 'aaaaaaaa',
            'password_confirmed': 'aaaaaaaa'
            }

        expected_exceptions = {
            'password': [
                'The password must have at least one capital letter.',
                'The password must have at least one number.',
                'The password must have at least one special character.'],
            'password_confirmed': [
                'The password must have at least one capital letter.',
                'The password must have at least one number.',
                'The password must have at least one special character.']
            }

        response = self.api.patch(url + USER_UUID + '/change-password', headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_password_with_other_user_uuid(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': data.get('password')
            })

        response = self.api.patch(url + '90b4f3b1-6fe2-4c6c-b0de-f56e0b6dd677' + '/change-password',
                                  headers=headers,
                                  json=data)

        self.assert_json_response(response, 'Not Found', 404, None)

    def test_update_password_without_user_uuid(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': data.get('password')
            })

        response = self.api.patch(url + '/change-password',
                                  headers=headers,
                                  json=data)

        self.assert_json_response(response, 'Not Found', 404, None)

    def test_update_password_without_user_uuid(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': data.get('password')
            })

        response = self.api.patch(url + '/change-password',
                                  headers=headers,
                                  json=data)

        self.assert_json_response(response, 'Not Found', 404, None)

    def test_update_password_without_header_authorizer(self):
        seed_users(self.db_connection)

        if headers.get('Authorization', None):
            headers.pop('Authorization')

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': data.get('password')
            })

        response = self.api.patch(url + USER_UUID + '/change-password', headers=headers, json=data)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_update_password_with_token_authorizer_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': 'Bearer HVXLzhVdz09OjUreS9CeVBwc3BFaUVrR3Y3VnF2RGsrVS9ZW'
            })

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': data.get('password')
            })

        response = self.api.patch(url + USER_UUID + '/change-password', headers=headers, json=data)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_update_password_with_token_type_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Basic {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('email')

        data.update({
            'password_confirmed': data.get('password')
            })

        response = self.api.patch(url + USER_UUID + '/change-password', headers=headers, json=data)
        self.assert_json_response(response, 'Unauthorized', 401, None)


def create_auth_token():
    add_claims = {
        'email': 'bgKCETfi8wXTNxfhKh7sHNcHoTLbNhHxwiJauwzoQQE='
        }

    return create_access_token(identity=USER_UUID, additional_claims=add_claims)
