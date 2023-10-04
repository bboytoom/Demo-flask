from .. import BaseTestClass
from src.models.User import User


class TestUserModel(BaseTestClass):

    def test_database_insert_success(self):
        create_user = User.new_user(self.user_seed)
        self.assertTrue(create_user.save())

    def test_database_insert_without_name(self):
        seed = self.user_seed
        seed.pop('name')

        create_user = User.new_user(seed)

        self.assertFalse(create_user.save())

    def test_database_retrieve_user(self):
        get_web_identifier = self.user_seed
        create_user = User.new_user(get_web_identifier)
        create_user.save()

        identifier = get_web_identifier.get('web_identifier', None)
        user = User.retrieve_user(identifier)

        self.assertEqual(user.web_identifier, identifier)
