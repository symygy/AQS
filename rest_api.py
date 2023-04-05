from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import json
from bson.json_util import dumps

from AQS.aqs_db import find_docs_by_date, find_docs_by_name, find_docs_by_id, find_docs_by_date_range

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


def abort_if_no_data_found(data: list):
    if not data:
        abort(404, ExceptionKey="No data found")

# prawdopodobnie do usuniecia
# def parse_data_from_mongo(data):
#     return json.loads(dumps(data))

query_args = reqparse.RequestParser()
query_args.add_argument('start', type=str)
query_args.add_argument('end', type=str)


class AirQualitySearchDate(Resource):
    @marshal_with(data_fields)
    def get(self, value):
        data = find_docs_by_date(value)
        abort_if_no_data_found(data)
        return data


class AirQualitySearchName(Resource):
    @marshal_with(data_fields)
    def get(self, name):
        data = find_docs_by_name(name)
        abort_if_no_data_found(data)
        return data


class AirQualitySearchId(Resource):
    @marshal_with(data_fields)
    def get(self, value):
        data = find_docs_by_id(value)
        abort_if_no_data_found(data)
        return data


class AirQualitySearchDateRange(Resource):
    @marshal_with(data_fields)
    #TODO jak przesylac przedzial daty?
    def get(self, name):
        args = query_args.parse_args()
        data = find_docs_by_date_range(args['start'], args['end'], name)
        abort_if_no_data_found(data)
        return data


api.add_resource(AirQualitySearchDate, '/search/date/<string:value>')
api.add_resource(AirQualitySearchName, '/search/name/<string:name>')
api.add_resource(AirQualitySearchId, '/search/id/<string:value>')
api.add_resource(AirQualitySearchDateRange, '/search/daterange/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)


# return parse_data_from_mongo(find_docs_by_date('2023-04-02'))
# 642944be4ad1ca6a305e25d0
