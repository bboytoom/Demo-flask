import uuid

from faker import Faker
from random import choice

fake = Faker()

client_uuid_array = [
    'ONBOARDING_STEP_ONE',
    'ONBOARDING_STEP_TWO'
    ]


def create_user() -> dict:
    return {
        'name': fake.name(),
        'web_identifier': str(uuid.uuid4()),
        'onboarding': choice(client_uuid_array),
        'status': True
        }
