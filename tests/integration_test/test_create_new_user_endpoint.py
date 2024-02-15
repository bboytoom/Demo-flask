import uuid
from src.models.User import User
from tests import BaseTestClass

url = '/api/v1/users'
headers = {'Content-Type': 'application/json'}


class TestCreateNewUserEndpoint(BaseTestClass):

    def test_create_new_user_success(self):
        response = self.api.post(url,  headers=headers, json=self.seed_payloads_new_user)
        result = response.get_json()

        user_exists = self.db_connection.session.query(User)\
            .filter(User.uuid == result.get('user_uuid'))\
            .first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(user_exists.uuid, result.get('user_uuid'))

    def test_create_new_user_duplicate(self):
        arrange = {
            'web_identifier': uuid.UUID('ecbe0d85-38ec-4b8c-ad90-76146804d9df'),
            'name': 'test',
            'last_name': 'Chapman',
            'birth_day': '1944-10-19',
            'status': True
            }

        user = User.new_user(arrange)
        user.save()

        arrange.pop('status')
        response = self.api.post(url,  headers=headers, json=arrange)

        self.assertEqual(response.status_code, 422)

    def _test_create_new_user_empty_data(self):
        fail_payload = {}

        response = self.api.post(url,  headers=headers, json=fail_payload)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 422)

        self.assertIn("['Missing data for required field.']", str(response_data))
        self.assertIn("['Missing data for required field.']", str(response_data))

    def _test_create_new_user_web_identifier_no_valid(self):
        fail_payload = {
            'web_identifier': 123,
            'name': 'blisa'
            }

        response = self.api.post(url,  headers=headers, json=fail_payload)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertIn("{'web_identifier': ['Not a valid UUID.']}", str(response_data))

    def _test_create_new_user_name_no_valid(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload['name'] = 123

        response = self.api.post(url,  headers=headers, json=fail_payload)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertIn("{'name': ['Not a valid string.']}", str(response_data))

    def _test_create_new_user_max_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload['name'] = 'sdkdkdflkmvdlfmldskdknfknkvfkdfkvkfnkfksñsñs'

        response = self.api.post(url,  headers=headers, json=fail_payload)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertIn("{'name': ['Length must be between 2 and 25.']}", str(response_data))

    def _test_create_new_user_min_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload['name'] = 'a'

        response = self.api.post(url,  headers=headers, json=fail_payload)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertIn("{'name': ['Length must be between 2 and 25.']}", str(response_data))

    def _test_create_new_user_without_header_json(self):
        response = self.api.post(url,
                                 headers={'Content-Type': 'application/xml'},
                                 json=self.seed_payloads_new_user)

        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('Content-Type not supported!', str(response_data))
