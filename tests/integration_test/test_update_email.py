from flask_jwt_extended import create_access_token

from tests import BaseTestClass
from tests.seed import seed_users

url = '/api/v1/users/'
headers = {'Content-Type': 'application/json'}
USER_UUID = '9bd82d2d-647f-4896-81ce-8055da610451'


class TestUpdateEmail(BaseTestClass):

    def test_update_email_success(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('password')

        expected = {
            'email': data.get('email'),
            'uuid': USER_UUID
            }

        response = self.api.patch(url + USER_UUID + '/change-email', headers=headers, json=data)
        self.assert_json_response(response, 'Successful request', 200, expected)

    def test_update_email_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('password')

        data.update({
            'email': 'test_email.com'
            })

        expected_exceptions = {
            'email': ['Not a valid email address.']
            }

        response = self.api.patch(url + USER_UUID + '/change-email', headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_email_without_field(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        expected_exceptions = {
            'email': ['Missing data for required field.']
            }

        response = self.api.patch(url + USER_UUID + '/change-email', headers=headers, json={})
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_email_with_other_user_uuid(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('password')

        response = self.api.patch(url + '90b4f3b1-6fe2-4c6c-b0de-f56e0b6dd677' + '/change-email',
                                  headers=headers,
                                  json=data)

        self.assert_json_response(response, 'Not Found', 404, None)

    def test_update_email_without_user_uuid(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('password')

        response = self.api.patch(url + '/change-email',
                                  headers=headers,
                                  json=data)

        self.assert_json_response(response, 'Not Found', 404, None)

    def test_update_email_without_header_authorizer(self):
        seed_users(self.db_connection)

        if headers.get('Authorization', None):
            headers.pop('Authorization')

        data = self.seed_payloads_password
        data.pop('password')

        response = self.api.patch(url + USER_UUID + '/change-email', headers=headers, json=data)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_update_password_with_authorizer_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': 'Bearer HVXLzhVdz09OjUreS9CeVBwc3BFaUVrR3Y3VnF2RGsrVS9ZW'
            })

        data = self.seed_payloads_password
        data.pop('password')

        response = self.api.patch(url + USER_UUID + '/change-email', headers=headers, json=data)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_update_password_with_authorizer_type_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Basic {create_auth_token()}'
            })

        data = self.seed_payloads_password
        data.pop('password')

        response = self.api.patch(url + USER_UUID + '/change-email', headers=headers, json=data)
        self.assert_json_response(response, 'Unauthorized', 401, None)


def create_auth_token():
    add_claims = {
        'email': 'bgKCETfi8wXTNxfhKh7sHNcHoTLbNhHxwiJauwzoQQE='
        }

    return create_access_token(identity=USER_UUID, additional_claims=add_claims)
