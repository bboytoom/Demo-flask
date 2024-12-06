from src.models.user import User

from tests import BaseTestClass

url = '/api/v1/sing_up'
headers = {'Content-Type': 'application/json'}


class TestSingUp(BaseTestClass):

    def test_sing_up_success(self):
        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=self.seed_payloads_new_user)
        response_data = response.get_json()

        user_exists = self.db_connection.session.query(User)\
            .filter(User.uuid == response_data.get('user_uuid'))\
            .first()

        self.assert_json_response(response, 'Successful request', 201, None)
        self.assertEqual(user_exists.uuid, response_data.get('user_uuid'))

    def test_sing_up_exists_user(self):
        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=self.seed_payloads_new_user)
        response = self.api.post(url,  headers=headers, json=self.seed_payloads_new_user)

        self.assert_json_response(response, 'Conflict', 409, None)

    def test_sing_up_without_birth_day(self):
        arrange = self.seed_payloads_new_user
        arrange.pop('birth_day')

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=arrange)
        response_data = response.get_json()

        user_exists = self.db_connection.session.query(User)\
            .filter(User.uuid == response_data.get('user_uuid'))\
            .first()

        self.assert_json_response(response, 'Successful request', 201, None)
        self.assertEqual(user_exists.uuid, response_data.get('user_uuid'))

    def test_sing_up_without_email(self):
        arrange = self.seed_payloads_new_user
        arrange.pop('email')

        expected_exceptions = {
            'email': ['Missing data for required field.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=arrange)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_with_email_wrong(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'email': 'testemail.com'
            })

        expected_exceptions = {
            'email': ['Not a valid email address.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_without_password(self):
        arrange = self.seed_payloads_new_user
        arrange.pop('password')

        expected_exceptions = {
            'password': ['Missing data for required field.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=arrange)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_with_password_8_characters(self):
        fake_data = self.seed_payloads_new_user
        incorrect_test = ['a', 'T5tP@0r']

        expected_exceptions = {
            'password': ['Length must be between 8 and 30.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        for item in incorrect_test:
            fake_data['password'] = item

            response = self.api.post(url,  headers=headers, json=fake_data)
            self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_with_password_capital_letter(self):
        fake_data = self.seed_payloads_new_user
        incorrect_test = ['te5tp@ssw0rd', 'te5tp@ ssw0rd']

        expected_exceptions = {
            'password': ['The password must have at least one capital letter.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        for item in incorrect_test:
            fake_data['password'] = item

            response = self.api.post(url,  headers=headers, json=fake_data)
            self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_with_password_lower_letter(self):
        fake_data = self.seed_payloads_new_user
        incorrect_test = ['TE5TP@SSW0RD', 'TE5TP@ SSW0RD']

        expected_exceptions = {
            'password': ['The password must have at least one lowercase letter.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        for item in incorrect_test:
            fake_data['password'] = item

            response = self.api.post(url,  headers=headers, json=fake_data)
            self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_with_password_number(self):
        fake_data = self.seed_payloads_new_user
        incorrect_test = ['teStp@sswOrd', 'teStp@ sswOrd']

        expected_exceptions = {
            'password': ['The password must have at least one number.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        for item in incorrect_test:
            fake_data['password'] = item

            response = self.api.post(url,  headers=headers, json=fake_data)
            self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_with_password_special_characters(self):
        fake_data = self.seed_payloads_new_user
        incorrect_test = ['Te5tPassw0rd', 'Te5t Passw0rd']

        expected_exceptions = {
            'password': ['The password must have at least one special character.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        for item in incorrect_test:
            fake_data['password'] = item

            response = self.api.post(url,  headers=headers, json=fake_data)
            self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_empty_data(self):
        fail_payload = {}

        expected_exceptions = {
            'last_name': ['Missing data for required field.'],
            'name': ['Missing data for required field.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_name_and_last_name_no_valid(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'name': 123,
            'last_name': 456
            })

        expected_exceptions = {
            'last_name': ['Not a valid string.'],
            'name': ['Not a valid string.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_max_characters_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'name': 'sdkdkdflkmvdlfmldskdknfknkvfkdf'
            })

        expected_exceptions = {
            'name': ['Length must be between 2 and 30.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_min_characters_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'name': 'a'
            })

        expected_exceptions = {
            'name': ['Length must be between 2 and 30.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_max_characters_last_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'last_name': 'sdkdkdflkmvdlfmldskdknfknkvfkdfsdkdkdflkmvdlfmldskdknfknkvfkdfsdkdkdflk'
            })

        expected_exceptions = {
            'last_name': ['Length must be between 2 and 70.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_min_characters_last_name(self):
        fail_payload = self.seed_payloads_new_user
        fail_payload.update({
            'last_name': 'a'
            })

        expected_exceptions = {
            'last_name': ['Length must be between 2 and 70.']
            }

        headers.update({
            'Authorization': f'Basic {self.credentials}'
            })

        response = self.api.post(url,  headers=headers, json=fail_payload)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)

    def test_sing_up_without_authorized(self):
        headers.pop('Authorization')

        response = self.api.post(url, headers=headers, json=self.seed_payloads_new_user)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_sing_up_with_authorized_bad_token(self):
        headers.update({
            'Authorization': 'Basic HVXLzhVdz09OjUreS9CeVBwc3BFaUVrR3Y3VnF2RGsrVS9ZW'
            })

        response = self.api.post(url, headers=headers, json=self.seed_payloads_new_user)
        self.assert_json_response(response, 'Unauthorized', 401, None)

    def test_sing_up_without_header_json(self):
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': f'Basic {self.credentials}'}

        response = self.api.post(url, headers=headers, json=self.seed_payloads_new_user)
        self.assert_json_response(response, 'Bad Request', 400, None)
