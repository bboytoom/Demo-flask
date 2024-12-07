from collections import OrderedDict

from tests import BaseTestClass
from tests.seed import seed_users

from src.services import UserService


class TestUserService(BaseTestClass):

    def test_retrieve_success(self):
        seed_users(self.db_connection)

        user = UserService.retrieve('9bd82d2d-647f-4896-81ce-8055da610451')

        self.assertIsInstance(user, OrderedDict)
        self.assertEqual(dict(user), self.response_user)

    def test_retrieve_user_uuid_fail(self):
        seed_users(self.db_connection)

        user = UserService.retrieve('c5244bd5-2d6b-474b-91e8-dfb6861e2b32')
        self.assertEqual(user, {})

    def test_retrieve_user_uuid_null(self):
        seed_users(self.db_connection)

        user = UserService.retrieve(None)
        self.assertEqual(user, {})

    def test_retrieve_user_uuid_empty(self):
        seed_users(self.db_connection)

        user = UserService.retrieve('')
        self.assertEqual(user, {})

    def test_create_success(self):
        data = {
            'birth_day': '1934-03-16',
            'email': 'moniqueweaver@example.com',
            'last_name': 'Hill',
            'name': 'Kimberly',
            'password': 'Te5tP@ssw0rd!!'
            }

        user = UserService.create(data)
        exists_user_in_db = exists_user_uuid(self.db_connection, user.get('uuid'))

        self.assertIsInstance(user, OrderedDict)
        self.assertTrue(exists_user_in_db)

    def test_create_twice_success(self):
        data_one = {
            'birth_day': '1934-03-16',
            'email': 'moniqueweaver@example.com',
            'last_name': 'Hill',
            'name': 'Kimberly',
            'password': 'Te5tP@ssw0rd!!'
            }

        UserService.create(data_one)

        data_two = {
            'birth_day': '1934-03-16',
            'email': 'moniqueweaver@example.com',
            'last_name': 'Hill',
            'name': 'Kimberly',
            'password': 'Te5tP@ssw0rd!!'
            }

        user = UserService.create(data_two)
        self.assertEqual(user.get('code'), 409)

    def test_create_birth_day_null(self):
        data = {
            'birth_day': None,
            'email': 'moniqueweaver@example.com',
            'last_name': 'Hill',
            'name': 'Kimberly',
            'password': 'Te5tP@ssw0rd!!'
            }

        user = UserService.create(data)
        exists_user_in_db = exists_user_uuid(self.db_connection, user.get('uuid'))

        self.assertIsInstance(user, OrderedDict)
        self.assertTrue(exists_user_in_db)

    def test_create_birth_day_empty(self):
        data = {
            'birth_day': '',
            'email': 'moniqueweaver@example.com',
            'last_name': 'Hill',
            'name': 'Kimberly',
            'password': 'Te5tP@ssw0rd!!'
            }

        user = UserService.create(data)
        exists_user_in_db = exists_user_uuid(self.db_connection, user.get('uuid'))

        self.assertIsInstance(user, OrderedDict)
        self.assertTrue(exists_user_in_db)

    def test_create_without_birth_day(self):
        data = {
            'email': 'moniqueweaver@example.com',
            'last_name': 'Hill',
            'name': 'Kimberly',
            'password': 'Te5tP@ssw0rd!!'
            }

        user = UserService.create(data)
        exists_user_in_db = exists_user_uuid(self.db_connection, user.get('uuid'))

        self.assertIsInstance(user, OrderedDict)
        self.assertTrue(exists_user_in_db)

    def test_create_without_email(self):
        data = {
            'birth_day': '1934-03-16',
            'last_name': 'Hill',
            'name': 'Kimberly',
            'password': 'Te5tP@ssw0rd!!'
            }

        user = UserService.create(data)
        self.assertEqual(user, {})

    def test_create_without_name(self):
        data = {
            'email': 'moniqueweaver@example.com',
            'birth_day': '1934-03-16',
            'last_name': 'Hill',
            'password': 'Te5tP@ssw0rd!!'
            }

        user = UserService.create(data)
        self.assertEqual(user, {})

    def test_create_without_password(self):
        data = {
            'email': 'moniqueweaver@example.com',
            'birth_day': '1934-03-16',
            'last_name': 'Hill',
            'name': 'Kimberly'
            }

        user = UserService.create(data)
        self.assertEqual(user, {})

    def test_create_without_last_name(self):
        data = {
            'email': 'moniqueweaver@example.com',
            'birth_day': '1934-03-16',
            'name': 'Kimberly',
            'password': 'Te5tP@ssw0rd!!'
            }

        user = UserService.create(data)
        self.assertEqual(user, {})


def exists_user_uuid(db, _user_uuid: str) -> bool:
    from src.models import User

    result = db.session.query(User).filter(User.uuid == _user_uuid).first()
    return False if not result else True
