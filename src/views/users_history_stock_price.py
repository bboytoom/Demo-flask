from flask import jsonify, abort, request
from flask.views import MethodView

from src.models.UserHistoricalStockPrice import UserHistoricalStockPrice
from src.schemas.stock_history_schema import StockHistorySchema, serializer_history_prices_schema
from src.helpers.read_csv_from_endpoint import file_data_read_from_csv
from src.views.decorators.endpoint_validation_body import validator_body
from src.views.decorators.endpoint_validation_parameters import validate_user_identifier


class UsersHistoryStockPrice(MethodView):

    @validate_user_identifier
    def get(self, user):
        symbol = request.args.get('symbol_stock', None)

        prices = UserHistoricalStockPrice.search_history_price(user.web_identifier, symbol)
        return jsonify(data=serializer_history_prices_schema.dump(prices)), 200

    @validate_user_identifier
    @validator_body(StockHistorySchema)
    def post(self, data, user):
        symbol_stock = data.get('symbol_stock', None)

        get_stock = file_data_read_from_csv(symbol_stock, user.web_identifier)
        price = UserHistoricalStockPrice.new_price(get_stock)

        if not price.save():
            return abort(500, 'Error inserting')

        return jsonify(get_stock), 201
