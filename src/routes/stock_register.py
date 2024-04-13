from flask import Blueprint

from src.views.stock_register import StockRegister

stock_register = Blueprint('stock_register', __name__,  url_prefix='/api/v1/stock_history')

stock_register.add_url_rule(
    '',
    view_func=StockRegister.as_view('create_stock'),
    methods=['POST']
    )
