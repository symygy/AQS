from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient, GEO2D, GEOSPHERE

load_dotenv(find_dotenv())
password = os.environ.get('PASS')

connection_str = f'mongodb+srv://mkurek:{password}@aqs.bsjlrtb.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(connection_str)

dbs = client.list_database_names()

aqs_db = client.AQS


def build_search_query(args: dict) -> dict:
    query = {}

    if args['startDate']:
        query["$gte"] = args['startDate']

    if args['endDate']:
        query["$lte"] = args['endDate']

    if not query:
        query["$ne"] = ''

    return query


def insert_many_docs(documents: list) -> list:
    return aqs_db.gios.insert_many(documents).inserted_ids


def get_all_docs() -> list:
    return list(aqs_db.gios.find())


def find_docs_by_name(name: str, date_args: dict) -> list:
    return list(aqs_db.gios.find({"data_odczytu": build_search_query(date_args), "nazwa_stacji": f'{name}'}))


def find_docs_by_code(code: str, date_args: dict) -> list:
    return list(aqs_db.gios.find({"data_odczytu": build_search_query(date_args), "kod_stacji": f'{code}'}))


def find_docs_by_station_id(id: int, date_args: dict) -> list:
    return list(aqs_db.gios.find({"data_odczytu": build_search_query(date_args), "identyfikator_stacji": id}))


def find_coords_by_code(station_code: str) -> list:
    result = aqs_db.gios.find_one({"kod_stacji": f'{station_code}'})
    if result is not None:
        return result['lokalizacja']


def drop_collection() -> bool:
    return aqs_db.gios.drop()


def create_2d_index():
    return aqs_db.gios.create_index([("location", GEO2D)])


def create_2dsphere_index():
    return aqs_db.gios.create_index([("lokalizacja", GEOSPHERE)])


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
                "key": "lokalizacja",
                "distanceField": "distance",
                "minDistance": dist_args["minDist"],
                "maxDistance": dist_args["maxDist"],
                "spherical": True
            }
        },
        {
            "$sort": {"data_odczytu": -1}
        },
        {
            "$group": {
                "_id": {"station": "$kod_stacji", "pollutant": "$wskaznik_kod"},
                "maxDocument": {"$first": "$$ROOT"}
            }
        },
        {
            "$replaceRoot": {
                "newRoot": "$maxDocument"
            }
        },
        {
            "$sort": {"kod_stacji": 1}
        },
    ])

    return list(results)
