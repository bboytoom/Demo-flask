import unittest

from src import create_app


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

    def tearDown(self):
        pass
