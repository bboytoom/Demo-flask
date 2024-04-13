from tests import BaseTestClass

url = '/api/v1/stock_history'
headers = {'Content-Type': 'application/json'}


class TestNewStockRegister(BaseTestClass):

    def test_new_stock_register_without_user(self):
        expected_exceptions = {
            'user_uuid': ['The user_uuid does not exists.']
            }

        response = self.api.post(url,  headers=headers, json=self.seed_payload_stock_register)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)
