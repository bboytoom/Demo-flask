import uuid
from src.models.User import User
from tests import BaseTestClass

url = '/api/v1/users'
headers = {'Content-Type': 'application/json'}


class TestCreateNewUserEndpoint(BaseTestClass):

    def test_create_new_user_success(self):
        response = self.api.post(url,  headers=headers, json=self.seed_payloads_new_user)
        response_data = response.get_json()

        user_exists = self.db_connection.session.query(User)\
            .filter(User.uuid == response_data.get('user_uuid'))\
            .first()

        self.assert_json_response(response, 'Successful request', 201, None)
        self.assertEqual(user_exists.uuid, response_data.get('user_uuid'))

    def test_create_new_user_success_without_birth_day(self):
        arrange = self.seed_payloads_new_user
        arrange.pop('birth_day')

        response = self.api.post(url,  headers=headers, json=arrange)
        response_data = response.get_json()

        user_exists = self.db_connection.session.query(User)\
            .filter(User.uuid == response_data.get('user_uuid'))\
            .first()

        self.assert_json_response(response, 'Successful request', 201, None)
        self.assertEqual(user_exists.uuid, response_data.get('user_uuid'))

    def test_create_new_user_duplicate(self):
        arrange = {
            'web_identifier': uuid.UUID('ecbe0d85-38ec-4b8c-ad90-76146804d9df'),
            'name': 'test',
            'last_name': 'Chapman',
            'birth_day': '1944-10-19',
            'status': True
            }

        expected_exceptions = {
            'web_identifier': ['The web_identifier must be unique.']
            }

        user = User.new_user(arrange)
        user.save()

        arrange.pop('status')
        response = self.api.post(url,  headers=headers, json=arrange)

        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_create_new_user_empty_data(self):
        fail_payload = {}

        expected_exceptions = {
            'last_name': ['Missing data for required field.'],
            'name': ['Missing data for required field.'],
            'web_identifier': ['Missing data for required field.']
            }

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_create_new_user_web_identifier_no_valid(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'web_identifier': 123
            })

        expected_exceptions = {
            'web_identifier': ['Not a valid UUID.']
            }

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_create_new_user_name_and_last_name_no_valid(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'name': 123,
            'last_name': 456
            })

        expected_exceptions = {
            'last_name': ['Not a valid string.'],
            'name': ['Not a valid string.']
            }

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_create_new_user_max_characters_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'name': 'sdkdkdflkmvdlfmldskdknfknkvfkdf'
            })

        expected_exceptions = {
            'name': ['Length must be between 2 and 30.']
            }

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_create_new_user_min_characters_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'name': 'a'
            })

        expected_exceptions = {
            'name': ['Length must be between 2 and 30.']
            }

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_create_new_user_max_characters_last_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'last_name': 'sdkdkdflkmvdlfmldskdknfknkvfkdfsdkdkdflkmvdlfmldskdknfknkvfkdfsdkdkdflk'
            })

        expected_exceptions = {
            'last_name': ['Length must be between 2 and 70.']
            }

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_create_new_user_min_characters_last_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'last_name': 'a'
            })

        expected_exceptions = {
            'last_name': ['Length must be between 2 and 70.']
            }

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_create_new_user_without_header_json(self):
        response = self.api.post(url,
                                 headers={'Content-Type': 'application/xml'},
                                 json=self.seed_payloads_new_user)

        self.assert_json_response(response, 'Bad Request', 400, None)
