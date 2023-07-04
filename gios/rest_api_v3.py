from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from AQS.gios.aqs_db import find_docs_by_code, find_docs_by_station_id, find_coords_by_code, find_near_stations

data_fields = {
    '_id': fields.String,
    'identyfikator_stacji': fields.Integer,
    'kod_stacji': fields.String,
    'nazwa_stacji': fields.String,
    'identyfikator_stanowiska': fields.Integer,
    'wskaznik': fields.String,
    'wskaznik_kod': fields.String,
    'data_odczytu': fields.String,
    'odczyt': fields.Float,
    'lokalizacja': fields.List(fields.String),
}

app = Flask(__name__)
api = Api(app)

def abort_if_no_data_found(data: list):
    if not data:
        abort(404, ExceptionKey="No data found")

date_args = reqparse.RequestParser()
date_args.add_argument('startDate', type=str, location='args')
date_args.add_argument('endDate', type=str, location='args')

range_args = reqparse.RequestParser()
range_args.add_argument('minDist', type=int, location='args', required = True, help='Providing minDist in meters is required')
range_args.add_argument('maxDist', type=int, location='args', required = True, help='Providing maxDist in meters is required')

class StationsByCode(Resource):
    @marshal_with(data_fields)
    def get(self, station_code):
        o_args = date_args.parse_args()
        data = find_docs_by_code(station_code, o_args)
        abort_if_no_data_found(data)
        return data

class StationsById(Resource):
    @marshal_with(data_fields)
    def get(self, station_id):
        o_args = date_args.parse_args()
        data = find_docs_by_station_id(station_id, o_args)
        abort_if_no_data_found(data)
        return data

class StationsByRange(Resource):
    @marshal_with(data_fields)
    def get(self, station_code):
        station_coords = find_coords_by_code(station_code)
        abort_if_no_data_found(station_coords)

        r_args = range_args.parse_args()
        data = find_near_stations(station_coords, r_args)
        abort_if_no_data_found(data)
        return data

api.add_resource(StationsByCode, '/v1/stations/code/<string:station_code>')
api.add_resource(StationsById, '/v1/stations/id/<int:station_id>')
api.add_resource(StationsByRange, '/v1/stations/range/<string:station_code>/')

if __name__ == '__main__':
    app.run(debug=True)