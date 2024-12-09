from faker import Faker

fake = Faker()


def payload_example() -> dict:
    return {
        'example': fake.email()
        }


def result_example() -> dict:
    return {
        'example': fake.email()
        }
