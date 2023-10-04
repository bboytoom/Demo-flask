from .. import BaseTestClass
from src.helpers.read_csv_from_endpoint import file_data_read_from_csv


class TestDataSource(BaseTestClass):

    def test_file_data_read_success(self):
        data = file_data_read_from_csv(self.url_base % ('AAPL'))

        self.assertIsInstance(data, dict)

    def test_does_not_exist_data_in_file(self):
        data = file_data_read_from_csv(self.url_base % ('NOEXIST'))

        self.assertIsNone(data)

    def test_url_does_not_exists(self):
        data = file_data_read_from_csv(self.url_fail)

        self.assertIsNone(data)

    def test_url_timeout(self):
        data = file_data_read_from_csv(self.url_timeout)

        self.assertIsNone(data)
