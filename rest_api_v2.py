from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

from AQS.aqs_db import find_docs_by_name, find_docs_by_id, get_all_docs, find_docs_by_area_code, find_near_stations, \
    find_coords_by_name

reading_fields = {
    '_id': fields.String,
    'nom_dept': fields.String,
    'nom_com': fields.String,
    'insee_com': fields.Integer,
    'nom_station': fields.String,
    'code_station': fields.String,
    'influence': fields.Integer,
    'nom_poll': fields.String,
    'valeur': fields.Integer,
    'unite': fields.String,
    'date_debut': fields.String,
    'date_fin': fields.String,
    'statut_valid': fields.String,
    'location': fields.List(fields.String),
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

class AirQualitySearchName(Resource):
    @marshal_with(reading_fields)
    def get(self, station_name):
        o_args = date_args.parse_args()
        data = find_docs_by_name(station_name, o_args)
        abort_if_no_data_found(data)
        return data

class AirQualitySearchAreaCode(Resource):
    @marshal_with(reading_fields)
    def get(self, area_code):
        o_args = date_args.parse_args()
        data = find_docs_by_area_code(area_code, o_args)
        abort_if_no_data_found(data)
        return data

class AirQualitySearchInRange(Resource):
    @marshal_with(reading_fields)
    def get(self, station_name):
        station_coords = find_coords_by_name(station_name)
        abort_if_no_data_found(station_coords)

        r_args = range_args.parse_args()
        data = find_near_stations(station_coords, r_args)
        abort_if_no_data_found(data)
        print(data)
        return data

api.add_resource(AirQualitySearchName, '/v1/stations/history/<string:station_name>')
api.add_resource(AirQualitySearchAreaCode, '/v1/stations/area/<int:area_code>')
api.add_resource(AirQualitySearchInRange, '/v1/stations/range/<string:station_name>/')

if __name__ == '__main__':
    app.run(debug=True)