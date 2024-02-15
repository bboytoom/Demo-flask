import unittest

from src import create_app
from src.config.sqlalchemy_db import db
from tests.factory_test import create_user, \
    create_history_price_to_user, \
    payload_create_new_user


class BaseTestClass(unittest.TestCase):

    # Code that is executed before each test
    def setUp(self):
        self.app = create_app()
        self.db_connection = db
        # Api
        self.api = self.app.test_client()

        # Seed
        self.user_seed = create_user()
        self.history_price_seed = create_history_price_to_user()
        self.seed_payloads_new_user = payload_create_new_user()

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
