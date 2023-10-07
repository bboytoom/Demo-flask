from tests import BaseTestClass
from src.models.User import User


class TestUser(BaseTestClass):

    def test_insert_data_success(self):
        data_to_insert = self.user_seed
        user = User.new_user(data_to_insert)

        save_user = user.save()

        self.assertEqual(
            save_user.web_identifier,
            str(data_to_insert.get('web_identifier')))

    def test_insert_empty_data(self):
        from sqlalchemy.exc import NoResultFound

        with self.assertRaises(NoResultFound) as context:
            user = User.new_user({})
            user.save()

        self.assertEqual(
            str(context.exception),
            'The model is empty'
            )

    def test_insert_insert_identifier_empty(self):
        with self.assertRaises(ValueError) as context:
            user = User.new_user({'name': 'test'})
            user.save()

        self.assertEqual(
            str(context.exception),
            'The web_identifier is empty'
            )

    def test_insert_insert_name_empty(self):
        with self.assertRaises(ValueError) as context:
            user = User.new_user({'web_identifier': '0872f892-6cc9-4477-b785-5a8f82303334'})
            user.save()

        self.assertEqual(
            str(context.exception),
            'The name is empty'
            )

    def test_is_not_uuid_identifier(self):
        with self.assertRaises(ValueError) as context:
            user = User.new_user({
                'web_identifier': '0872f892-6cc9-4477-b785',
                'name': 'test'
                })

            user.save()

        self.assertEqual(
            str(context.exception),
            'The web_identifier does not uuid'
            )

    def test_max_characters_name(self):
        with self.assertRaises(ValueError) as context:
            user = User.new_user({
                'web_identifier': 'b5817c6b-92ee-4ae9-89b2-a6ca02476845',
                'name': 'test_test_test_test_test_test_test_test_test_test_test'
                })

            user.save()

        self.assertEqual(
            str(context.exception),
            'The name must be between 2 to 25 characters'
            )

    def test_min_characters_name(self):
        with self.assertRaises(ValueError) as context:
            user = User.new_user({
                'web_identifier': '6af271c5-54ad-4800-90d8-c0691b75839c',
                'name': 'a'
                })

            user.save()

        self.assertEqual(
            str(context.exception),
            'The name must be between 2 to 25 characters'
            )

    def test_insert_duplicate_web_identifier(self):
        data_to_insert = self.user_seed

        user_one = User.new_user(data_to_insert)
        user_one.save()

        with self.assertRaises(TypeError) as context:
            user_dos = User.new_user(data_to_insert)
            user_dos.save()

        self.assertEqual(
            str(context.exception),
            'Duplicated data in database'
            )
