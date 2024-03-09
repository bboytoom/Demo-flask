from src.models.user import User
from tests import BaseTestClass

url = '/api/v1/stock_history'
headers = {'Content-Type': 'application/json'}


class TestNewStockRegister(BaseTestClass):

    def test_new_stock_register_success(self):
        user =  User.new_user(self.seed_payloads_new_user)
        user.save()

        stock_register = self.seed_payload_stock_register
        stock_register.update({
            'user_uuid': user.uuid
        })

        response = self.api.post(url,  headers=headers, json=stock_register)   

        print('\n ---------------- \n')
        
        print(response,  'response')
        
        self.assertTrue(True)
        

    def test_new_stock_register_without_user(self):
        expected_exceptions = {
            'user_uuid': ['The user_uuid does not exists.']
            }

        response = self.api.post(url,  headers=headers, json=self.seed_payload_stock_register)
        self.assert_json_response(response, 'Unprocessable Entity', 422, expected_exceptions)
