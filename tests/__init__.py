import os
import unittest

from base64 import b64encode

from src import create_app
from src.config.databases import db
from src.helpers import CryptographyMessage

from tests.custom_asserts import CustomAsserts
from tests.factory_test import payload_create_new_user, payload_password, result_access_user


class BaseTestClass(unittest.TestCase, CustomAsserts):

    _security_field = CryptographyMessage()

    # Code that is executed before each test
    def setUp(self):
        self.app = create_app()
        self.db_connection = db
        qa_username = self._security_field.encrypt(os.environ.get('AUTH_USERNAME'))
        qa_password = self._security_field.encrypt(os.environ.get('AUTH_PASSWORD'))

        # Api
        self.api = self.app.test_client()

        # Seed
        self.seed_payloads_new_user = payload_create_new_user()
        self.seed_payloads_password = payload_password()

        # Responses
        self.response_access_user = result_access_user()

        # Auth
        credential_string = f'{(qa_username)}:{qa_password}'
        self.credentials = b64encode(credential_string.encode('utf-8')).decode('utf-8')

        # Context application
        self.app.app_context().push()
        db.create_all()

    # Code that is executed after each test
    def tearDown(self):
        try:
            db.session.remove()
            db.drop_all()
        except Exception as e:
            print(f"Error en tearDown: {str(e)}")
