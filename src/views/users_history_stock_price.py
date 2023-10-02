from flask import jsonify
from flask.views import MethodView


class UsersHistoryStockPrice(MethodView):

    def get(self, identifier):
        print(identifier)

        data = [
            {
                'symbol_stock': 'AAPL',
                'date_stock': '2023-09-29',
                'time_stock': '22:00:15',
                'open_price': 172.02,
                'high_price': 173.07,
                'low_price': 170.341,
                'close_price': 171.21
                }
            ]

        return jsonify(
            data=data
            ), 200

    def post(self, identifier):

        print(identifier)

        return jsonify(
            symbol='AAPL',
            open=172.02,
            high=173.07,
            low=170.341,
            close=171.21,
            date_stock='2023-09-29',
            time_stock='22:00:15',
            created_at='2023-09-29 22:00:15'
            ), 201
