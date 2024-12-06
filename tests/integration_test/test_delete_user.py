from flask_jwt_extended import create_access_token

from tests import BaseTestClass
from tests.seed import seed_users

url = '/api/v1/users/'
headers = {'Content-Type': 'application/json'}
USER_UUID = '9bd82d2d-647f-4896-81ce-8055da610451'


class TestDeleteUser(BaseTestClass):

    def test_delete_user_success(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        response = self.api.delete(url + USER_UUID,  headers=headers)
        self.assert_json_response(response, None, 204, None)

    def test_delete_user_without_user_uuid(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        response = self.api.delete(url,  headers=headers)
        self.assert_json_response(response, 'Not Found', 404, None)

    def test_delete_user_with_user_uuid_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': f'Bearer {create_auth_token()}'
            })

        response = self.api.delete(url + '90b4f3b1-6fe2-4c6c-b0de-f56e0b6dd677',
                                   headers=headers)

        self.assert_json_response(response, 'Not Found', 404, None)

    def test_delete_user_without_header_authorizer(self):
        seed_users(self.db_connection)

        if headers.get('Authorization', None):
            headers.pop('Authorization')

        response = self.api.delete(url + USER_UUID, headers=headers)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_delete_user_with_authorizer_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': 'Bearer HVXLzhVdz09OjUreS9CeVBwc3BFaUVrR3Y3VnF2RGsrVS9ZW'
            })

        response = self.api.delete(url + USER_UUID, headers=headers)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_delete_user_with_authorizer_type_fail(self):
        seed_users(self.db_connection)

        headers.update({
            'Authorization': 'Basic HVXLzhVdz09OjUreS9CeVBwc3BFaUVrR3Y3VnF2RGsrVS9ZW'
            })

        response = self.api.delete(url + USER_UUID, headers=headers)
        self.assert_json_response(response, 'Unauthorized', 401, None)


def create_auth_token():
    add_claims = {
        'email': 'bgKCETfi8wXTNxfhKh7sHNcHoTLbNhHxwiJauwzoQQE='
        }

    return create_access_token(identity=USER_UUID, additional_claims=add_claims)
