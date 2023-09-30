import unittest

from src import create_app


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

        self.url_base = 'https://stooq.com/q/l/?s=%s.us&f=sd2t2ohlcv&h&e=csv'
        self.url_fail = 'https://tedfdfst.com/'
        self.url_timeout = 'https://test.com/'

    def tearDown(self):
        pass
