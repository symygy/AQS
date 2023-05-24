from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import json
from bson.json_util import dumps

from AQS.aqs_db import find_docs_by_name, find_docs_by_id, get_all_docs

app = Flask(__name__)
api = Api(app)

info_fields = {
    'name': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'status': fields.Integer,
    'date': fields.String,
}

atmo_fields = {
    'no2': fields.Integer,
    'o3': fields.Integer,
    'pm10': fields.Integer,
    'pm25': fields.Integer,
    'so2': fields.Integer,
}

data_fields = {
    '_id': fields.String,
    'info': fields.Nested(info_fields),
    'atmo': fields.Nested(atmo_fields)
}

station_fields = {
    '_id': fields.String,
    'name': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'status': fields.Integer,
}


def abort_if_no_data_found(data: list):
    if not data:
        abort(404, ExceptionKey="No data found")


# prawdopodobnie do usuniecia
# def parse_data_from_mongo(data):
#     return json.loads(dumps(data))


optional_args = reqparse.RequestParser()
optional_args.add_argument('startDate', type=str, location='args')
optional_args.add_argument('endDate', type=str, location='args')


class AirQualitySearchName(Resource):
    @marshal_with(data_fields)
    def get(self, station_name):
        o_args = optional_args.parse_args()
        data = find_docs_by_name(station_name, o_args)
        abort_if_no_data_found(data)
        return data


class AirQualitySearchId(Resource):
    @marshal_with(data_fields)
    def get(self, id_value):
        data = find_docs_by_id(id_value)
        abort_if_no_data_found(data)
        return data


class AirQualityStations(Resource):
    @marshal_with(station_fields)
    def get(self):
        data = get_all_docs('stations')
        abort_if_no_data_found(data)
        return data


api.add_resource(AirQualitySearchName, '/v1/stations/history/<string:station_name>')
api.add_resource(AirQualitySearchId, '/v1/stations/<string:id_value>')
api.add_resource(AirQualityStations, '/v1/stations/')

if __name__ == '__main__':
    app.run(debug=True)
