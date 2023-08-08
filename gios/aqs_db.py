from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient, GEOSPHERE

load_dotenv(find_dotenv())
password = os.environ.get('PASS')

connection_str = f'mongodb+srv://mkurek:{password}@aqs.bsjlrtb.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(connection_str)

dbs = client.list_database_names()

aqs_db = client.AQS

collections = {
    'gios': aqs_db.gios,
    'gios_stations': aqs_db.gios_stations
}


def build_search_query(args: dict) -> dict:
    """ Returns query used for searching documents by date"""

    query = {}

    if args['startDate']:
        query["$gte"] = args['startDate']

    if args['endDate']:
        query["$lte"] = args['endDate']

    if not query:
        query["$ne"] = ''

    return query


def insert_many_docs(documents: list, col_name: str) -> list:
    """ Inserts many documents into collection and returns all inserted records ID"""
    return collections[col_name].insert_many(documents).inserted_ids


def get_all_docs() -> list:
    """ Returns all records from gios collection """
    return list(aqs_db.gios.find())


def get_all_stations() ->list:
    return list(aqs_db.gios_stations.find())


def find_docs_by_name(name: str, date_args: dict) -> list:
    """ Returns station found by station name """
    return list(aqs_db.gios.find({"measurement_date": build_search_query(date_args), "station_name": f'{name}'}))


def find_docs_by_code(code: str, date_args: dict) -> list:
    """ Returns station found by station code """
    return list(aqs_db.gios.find({"measurement_date": build_search_query(date_args), "station_code": f'{code}'}))


def find_docs_by_station_id(id: int, date_args: dict) -> list:
    """ Returns station found by ID """
    return list(aqs_db.gios.find({"measurement_date": build_search_query(date_args), "station_id": id}))


def find_coords_by_code(station_code: str) -> list:
    """ Returns station coordinates by station_code """
    result = aqs_db.gios.find_one({"station_code": f'{station_code}'})
    if result is not None:
        return result['location']


def drop_collection(col_name: str) -> bool:
    """ Drops 'gios' collection """
    return collections[col_name].drop()


def create_2dsphere_index():
    """ Creates 2dsphere index """
    return aqs_db.gios.create_index([("location", GEOSPHERE)])


def find_near_stations(coord: list, dist_args: dict):
    """
    :param coord: coordinates [long, lat] eg. [3.50804, 50.3585]
    :param dist_args: provided min_dist and max_dist in query params
    :return: list of readings - one document per pollutant with latest date
    """

    results = aqs_db.gios.aggregate([
        {
            "$geoNear": {
                "near": {"type": "Point", "coordinates": coord},
                "key": "location",
                "distanceField": "distance",
                "minDistance": dist_args["minDist"],
                "maxDistance": dist_args["maxDist"],
                "spherical": True
            }
        },
        {
            "$sort": {"measurement_date": -1}
        },
        {
            "$group": {
                "_id": {"station": "$station_code", "pollutant": "$pollutant_symbol"},
                "maxDocument": {"$first": "$$ROOT"}
            }
        },
        {
            "$replaceRoot": {
                "newRoot": "$maxDocument"
            }
        },
        {
            "$sort": {"station_code": 1}
        },
    ])

    return list(results)
