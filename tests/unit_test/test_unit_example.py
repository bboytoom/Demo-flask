from tests import BaseTestClass

"""
The test run
python -m unittest directory/test.py -k test_function
"""

class TestUnitExample(BaseTestClass):

    def test_example(self):
        self.assertTrue(True)
