import unittest

from src import create_app
from src.config.sqlalchemy_db import db
from tests.factory_test import create_user, create_history_price_to_user


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

        # Url seed
        self.url_base = 'https://stooq.com/q/l/?s=%s.us&f=sd2t2ohlcv&h&e=csv'
        self.url_fail = 'https://tedfdfst.com/'
        self.url_timeout = 'https://test.com/'

        # Seed
        self.user_seed = create_user()
        self.history_price_seed = create_history_price_to_user()

        # Contest application
        self.app.app_context().push()
        db.create_all()

    def tearDown(self):
        self.app.app_context().push()
        db.drop_all()
