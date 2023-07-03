from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

from AQS.aqs_db import find_docs_by_name, find_docs_by_id, get_all_docs, find_docs_by_area_code, find_near_stations, \
    find_coords_by_name

data_fields = {
    '_id': fields.String,
    'Identyfikator stacji': fields.Integer,
    'Kod stacji': fields.String,
    'Nazwa stacji': fields.String,
    'Identyfikator stanowiska': fields.Integer,
    'Wskaźnik': fields.String,
    'Jednostka': fields.String,
    'Data odczytu': fields.String,
    'Odczyt': fields.Float,
    'Lokalizacja': fields.List(fields.String),
}

app = Flask(__name__)
api = Api(app)

def abort_if_no_data_found(data: list):
    if not data:
        abort(404, ExceptionKey="No data found")

date_args = reqparse.RequestParser()
date_args.add_argument('startDate', type=str, location='args')
date_args.add_argument('endDate', type=str, location='args')

class AirQualitySearchName(Resource):
    @marshal_with(data_fields)
    def get(self, station_name):
        o_args = date_args.parse_args()
        data = find_docs_by_name(station_name, o_args)
        abort_if_no_data_found(data)
        return data

# class AirQualitySearchCode(Resource):
#     @marshal_with(data_fields)
#     def get(self, station_code):
#         o_args = date_args.parse_args()
#         data = find_docs_by_name(station_code, o_args)
#         abort_if_no_data_found(data)
#         return data

api.add_resource(AirQualitySearchName, '/v1/stations/name/<string:station_name>')
# api.add_resource(AirQualitySearchCode, '/v1/stations/name/<string:station_code>')

if __name__ == '__main__':
    app.run(debug=True)