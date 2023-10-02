from .. import BaseTestClass
from src.models.User import User
from src.models.UserHistoricalStockPrice import UserHistoricalStockPrice


class TestUserHistoryStockPriceModel(BaseTestClass):

    def test_database_insert_price_success(self):
        get_history = created_price_history(self)
        create_price = UserHistoricalStockPrice.new_price(get_history)

        self.assertTrue(create_price.save())

    def test_database_retrieve_price(self):
        get_history = created_price_history(self)

        create_price = UserHistoricalStockPrice.new_price(get_history)
        create_price.save()

        get_symbol = get_history.get('symbol_stock')
        web_identifier = get_history.get('web_identifier_uuid')

        price_history = UserHistoricalStockPrice.search_history_price(web_identifier, get_symbol)

        for price in price_history:
            self.assertEqual(get_symbol, price.symbol_stock)
            self.assertEqual(web_identifier, price.web_identifier_uuid)


def created_price_history(self):
    get_user = self.user_seed
    get_price_history = self.history_price_seed

    create_user = User.new_user(get_user)
    create_user.save()

    get_price_history.update({
        'web_identifier_uuid': get_user.get('web_identifier', None)
        })

    return get_price_history
