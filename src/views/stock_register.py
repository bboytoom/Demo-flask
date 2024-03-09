from flask import jsonify, abort
from flask.views import MethodView

from src.schemas.stock_register_schema import StockRegisterSchema
from src.views.decorators.endpoint_validation_body import validator_body


class StockRegister(MethodView):
    """
    Endpoint for register un price stock
    """

    @validator_body(StockRegisterSchema)
    def post(self, data):
        
        print(data, 'data')

        return jsonify(
            message='Successful request'
            ), 201
