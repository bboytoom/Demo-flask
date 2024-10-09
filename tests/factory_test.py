from faker import Faker

fake = Faker()


def payload_create_new_user() -> dict:
    return {
        'name': fake.first_name(),
        'last_name': fake.last_name(),
        'birth_day': str(fake.date_of_birth(minimum_age=18))
        }
