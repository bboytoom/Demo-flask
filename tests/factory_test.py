from faker import Faker

fake = Faker()


def payload_create_new_user() -> dict:
    return {
        'email': fake.email(),
        'password': 'Te5tP@ssw0rd!!',
        'name': fake.first_name(),
        'last_name': fake.last_name(),
        'birth_day': str(fake.date_of_birth(minimum_age=18))
        }


def payload_password() -> dict:
    return {
        'email': 'test@example.com',
        'password': 'Te5tP@ssw0rd!!'
        }


def payload_user_info() -> dict:
    return {
        'name': fake.first_name(),
        'last_name': fake.last_name(),
        'birth_day': str(fake.date_of_birth(minimum_age=18))
        }


def result_access_user() -> dict:
    return {
        'access_token': 'eyJhbGciOiJIUzUxMiIl3LTRkNWYtNGJkYDRVRmaTh3ZI8F35qj6LWNA2c1Jx0uvr14o',
        'birth_day': '2000-11-16',
        'expires_in': 10800,
        'last_name': 'ross',
        'name': 'blisa',
        'refresh_token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6he',
        'token_type': 'Bearer',
        'uuid': '9bd82d2d-647f-4896-81ce-8055da610451'
        }


def result_user() -> dict:
    return {
        'birth_day': '2000-11-16',
        'created_at': '2024-12-01T21:46:56',
        'email': 'test@example.com',
        'last_name': 'ross',
        'name': 'blisa',
        'updated_at': '2024-12-01T21:46:56',
        'uuid': '9bd82d2d-647f-4896-81ce-8055da610451'
        }
