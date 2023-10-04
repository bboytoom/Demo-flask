import uuid

from faker import Faker
from random import choice
from datetime import date, time

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


def create_history_price_to_user() -> dict:
    return {
        'symbol_stock': 'AAPL',
        'open_price': 172.02,
        'high_price': 173.07,
        'low_price': 170.341,
        'close_price': 171.21,
        'time_stock': time.fromisoformat('22:00:15'),
        'date_stock': date.fromisoformat('2023-09-29')
        }
