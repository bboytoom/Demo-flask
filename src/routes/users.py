from flask import Blueprint

from src.views.users import Users
from src.views.users_history_stock_price import UsersHistoryStockPrice

users = Blueprint('users', __name__,  url_prefix='/api/v1')

users.add_url_rule(
    '/users/<uuid:identifier>',
    view_func=Users.as_view('retrieve_user'),
    methods=['GET']
    )

users.add_url_rule(
    '/users',
    view_func=Users.as_view('create_user'),
    methods=['POST']
    )

users.add_url_rule(
    '/users/<uuid:identifier>/stock-history',
    view_func=UsersHistoryStockPrice.as_view('insert_stock_history'),
    methods=['POST']
    )

users.add_url_rule(
    '/users/<uuid:identifier>/stock-history',
    view_func=UsersHistoryStockPrice.as_view('retrieve_stock_history'),
    methods=['GET']
    )
