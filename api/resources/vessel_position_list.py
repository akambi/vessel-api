from flask_restful import reqparse, Resource, fields, marshal_with
from api.models import VesselPosition
from datetime import datetime
import re

def valid_datetime_type(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")

def valid_date_type(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%d")

def valid_decimal_type(decimal_str):
    if decimal_str.replace('.', '', 1).isdigit():
        return decimal_str
    raise ValueError('Value must be a decimal')

vessel_position_fields = {
    'id': fields.Integer,
    'vessel_id': fields.Integer,
    'latitude': fields.String,
    'longitude': fields.String,
    'received_time_utc': fields.DateTime
}

class VesselPositionList(Resource):
    def get(self):
        vessel_position_get_args = reqparse.RequestParser()
        vessel_position_get_args.add_argument(
            'dateFrom',
            required=True,
            location='args',
            type=valid_date_type
        )

        vessel_position_get_args.add_argument(
            'dateTo',
            required=True,
            location='args',
            type=valid_date_type
        )

        args = vessel_position_get_args.parse_args()
        return VesselPosition.get_vessels(args.dateFrom, args.dateTo)

    @marshal_with(vessel_position_fields)
    def post(self):
        vessel_position_post_args = reqparse.RequestParser()
        vessel_position_post_args.add_argument(
            'vessel_id',
            type=int,
            required=True,
            help="Vessel ID must be an integer!",
            location='form'
        )
        vessel_position_post_args.add_argument(
            'received_time_utc',
            required=True,
            type=valid_datetime_type,
            location='form'
        )
        vessel_position_post_args.add_argument(
            'latitude',
            required=True,
            type=valid_decimal_type,
            help="Latitude must be a decimal!",
            location='form'
        )
        vessel_position_post_args.add_argument(
            'longitude',
            required=True,
            type=valid_decimal_type,
            help="Longitude must be a decimal!",
            location='form'
        )

        args = vessel_position_post_args.parse_args()
        new_position = VesselPosition.create(**args)
        return new_position

