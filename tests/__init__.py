import os
import unittest

from base64 import b64encode

from src import create_app
from src.config.databases import db
from src.helpers import CryptographyMessage

from tests.custom_asserts import CustomAsserts
from tests.factory_test import payload_example, result_example


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
        self.seed_payloads_example = payload_example()

        # Responses
        self.result_example = result_example()

        # Auth
        credential_string = f'{(qa_username)}:{qa_password}'
        self.credentials = b64encode(credential_string.encode('utf-8')).decode('utf-8')

        # Context application
        self.app.app_context().push()
        db.create_all()

    # Code that is executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
