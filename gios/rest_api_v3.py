from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from AQS.gios.aqs_db import find_docs_by_code, find_docs_by_station_id, find_coords_by_code, find_near_stations, \
    get_all_stations
from AQS.gios.fetch_data_gios import get_stations
from kafka_producer import MessageProducer
from flask_cors import CORS

data_fields = {
    '_id': fields.String,
    'station_id': fields.Integer,
    'station_code': fields.String,
    'station_name': fields.String,
    'sensor_id': fields.Integer,
    'pollutant': fields.String,
    'pollutant_symbol': fields.String,
    'measurement_date': fields.String,
    'measurement_value': fields.Float,
    'location': fields.List(fields.String),
}

station_fields = {
    '_id': fields.String,
    'station_id': fields.Integer,
    'station_code': fields.String,
    'station_name': fields.String,
    'city_id': fields.Integer,
    'city': fields.String,
    'community': fields.String,
    'county': fields.String,
    'voivodeship': fields.String,
    'street': fields.String,
    'location': fields.List(fields.String),
}

app = Flask(__name__)
api = Api(app)
CORS(app)

def abort_if_no_data_found(data: list):
    if not data:
        abort(404, ExceptionKey="No data found")

date_args = reqparse.RequestParser()
date_args.add_argument('startDate', type=str, location='args')
date_args.add_argument('endDate', type=str, location='args')

range_args = reqparse.RequestParser()
range_args.add_argument('minDist', type=int, location='args', required = True, help='Providing minDist in meters is required')
range_args.add_argument('maxDist', type=int, location='args', required = True, help='Providing maxDist in meters is required')


class StationsAll(Resource):
    @marshal_with(station_fields)
    def get(self):
        data = get_all_stations()
        abort_if_no_data_found(data)
        return data

class StationsByCode(Resource):
    @marshal_with(data_fields)
    def get(self, station_code):
        o_args = date_args.parse_args()
        data = find_docs_by_code(station_code, o_args)
        abort_if_no_data_found(data)

        # message_producer.send_msg({'endpoint': '/v1/stations/code/', 'station_code': station_code, 'args': o_args})
        return data

class StationsById(Resource):
    @marshal_with(data_fields)
    def get(self, station_id):
        o_args = date_args.parse_args()
        data = find_docs_by_station_id(station_id, o_args)
        abort_if_no_data_found(data)

        # message_producer.send_msg({'endpoint': '/v1/stations/id/', 'station_id': station_id, 'args': o_args})
        return data

class StationsByRange(Resource):
    @marshal_with(data_fields)
    def get(self, station_code):
        station_coords = find_coords_by_code(station_code)
        abort_if_no_data_found(station_coords)

        r_args = range_args.parse_args()
        data = find_near_stations(station_coords, r_args)
        abort_if_no_data_found(data)

        # message_producer.send_msg({'endpoint': '/v1/stations/range/', 'station_code': station_code, 'args': r_args})
        return data

api.add_resource(StationsAll, '/v1/stations/')
api.add_resource(StationsByCode, '/v1/stations/code/<string:station_code>')
api.add_resource(StationsById, '/v1/stations/id/<int:station_id>')
api.add_resource(StationsByRange, '/v1/stations/range/<string:station_code>/')

if __name__ == '__main__':
    # broker = '192.168.1.26:9092'
    # topic = 'gios_atmo_data'
    # message_producer = MessageProducer(broker, topic)

    app.run(debug=True)