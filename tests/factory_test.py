from faker import Faker
from datetime import date, time

fake = Faker()


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


def payload_create_new_user() -> dict:
    return {
        'name': fake.first_name(),
        'last_name': fake.last_name(),
        'birth_day': str(fake.date_of_birth(minimum_age=18))
        }
