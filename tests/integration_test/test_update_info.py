from flask_jwt_extended import create_access_token

from tests import BaseTestClass
from tests.seed import seed_users

url = '/api/v1/users/'
headers = {'Content-Type': 'application/json'}
USER_UUID = '9bd82d2d-647f-4896-81ce-8055da610451'


class TestUpdateInfo(BaseTestClass):

    def test_update_info_success(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_user_info

        expected = {
            'birth_day': data.get('birth_day'),
            'last_name': data.get('last_name'),
            'name': data.get('name'),
            'uuid': USER_UUID
            }

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Successful request', 200, expected)

    def test_update_info_without_birth_day(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_user_info
        data.pop('birth_day')

        expected = {
            'birth_day': None,
            'last_name': data.get('last_name'),
            'name': data.get('name'),
            'uuid': USER_UUID
            }

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Successful request', 200, expected)

    def test_update_info_without_name(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_user_info
        data.pop('name')

        expected_exceptions = {
            'name': ['Missing data for required field.']
            }

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_info_without_last_name(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_user_info
        data.pop('last_name')

        expected_exceptions = {
            'last_name': ['Missing data for required field.']
            }

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_info_name_min_characters(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_user_info
        data.update({
            'name': 'a'
            })

        expected_exceptions = {
            'name': ['Length must be between 2 and 30.']
            }

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_info_last_name_min_characters(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_user_info
        data.update({
            'last_name': 'a'
            })

        expected_exceptions = {
            'last_name': ['Length must be between 2 and 70.']
            }

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_info_birth_day_fail_format(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_user_info

        invalid_birth_day = ['08-03-2008', 'a', 123, '98-03-23', 'test']

        for item in invalid_birth_day:
            data.update({
                'birth_day': item
                })

            expected_exceptions = {
                'birth_day': ['Not a valid date.']
                }

            response = self.api.patch(url + USER_UUID, headers=headers, json=data)
            self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_info_other_filed(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = {
            'birth': '2008-03-24',
            'lastname': 'test',
            'names': 'test',
            }

        expected_exceptions = {
            'birth': [
                'Unknown field.'
                ],
            'last_name': [
                'Missing data for required field.'
                ],
            'lastname': [
                'Unknown field.'
                ],
            'name': [
                'Missing data for required field.'
                ],
            'names': [
                'Unknown field.'
                ]
            }

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_update_info_without_user_uuid(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        data = self.seed_payloads_user_info

        response = self.api.patch(
            url + '90b4f3b1-6fe2-4c6c-b0de-f56e0b6dd677', headers=headers, json=data)
        self.assert_json_response(response, 'Not Found', 404, None)

    def test_update_info_with_user_uuid_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        response = self.api.get(url + '90b4f3b1-6fe2-4c6c-b0de-f56e0b6dd677',
                                headers=headers)

        self.assert_json_response(response, 'Not Found', 404, None)

    def test_update_info_without_header_authorizer(self):
        seed_users(self.db_connection)

        if headers.get('Authorization', None):
            headers.pop('Authorization')

        data = self.seed_payloads_user_info

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_update_info_with_authorizer_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': 'Bearer HVXLzhVdz09OjUreS9CeVBwc3BFaUVrR3Y3VnF2RGsrVS9ZW'
            })

        data = self.seed_payloads_user_info

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_update_info_with_authorizer_type_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Basic {create_auth_token()}'
            })

        data = self.seed_payloads_user_info

        response = self.api.patch(url + USER_UUID, headers=headers, json=data)
        self.assert_json_response(response, 'Unauthorized', 401, None)


def create_auth_token():
    add_claims = {
        'email': 'bgKCETfi8wXTNxfhKh7sHNcHoTLbNhHxwiJauwzoQQE='
        }

    return create_access_token(identity=USER_UUID, additional_claims=add_claims)
