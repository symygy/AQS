from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import json
from bson.json_util import dumps

from AQS.aqs_db import find_docs_by_date

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
    # '_id': fields.String,
    'info': fields.Nested(info_fields),
    'atmo': fields.Nested(atmo_fields)
}

def parse_data_from_mongo(data):
    return json.loads(dumps(data))

class AirQuality(Resource):
    @marshal_with(data_fields)
    def get(self):
       return find_docs_by_date('2023-04-02')


        # return parse_data_from_mongo(find_docs_by_date('2023-04-02'))

api.add_resource(AirQuality, '/stations/')

if __name__ == '__main__':
    app.run(debug=True)