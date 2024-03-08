from datetime import date, time
from flask import request
from marshmallow import Schema, fields, validate, pre_dump


class StockHistorySchema(Schema):
    class Meta:
        ordered = True

    web_identifier_uuid = fields.Str()

    symbol_stock = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=20)
            ]
        )

    open_price = fields.Float()
    high_price = fields.Float()
    low_price = fields.Float()
    close_price = fields.Float()

    date_stock = fields.Date('%Y-%m-%d')
    time_stock = fields.Time()

    @pre_dump
    def pre_dump(self, data, **kwargs):

        if request.method in ['GET']:
            return data

        return {
            'symbol_stock': data[0][:-3],
            'date_stock': date.fromisoformat(data[1]),
            'time_stock': time.fromisoformat(data[2]),
            'open_price': data[3],
            'high_price': data[4],
            'low_price': data[5],
            'close_price': data[6],
            'web_identifier_uuid': data[8]
            }
