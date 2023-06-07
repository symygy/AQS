from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient, UpdateOne, GEO2D, GEOSPHERE

load_dotenv(find_dotenv())
password = os.environ.get('PASS')

connection_str = f'mongodb+srv://mkurek:{password}@aqs.bsjlrtb.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(connection_str)

dbs = client.list_database_names()

aqs_db = client.AQS

collections = {
    'atmo': aqs_db.AQS,
    'stations': aqs_db.stations,
    'exp': aqs_db.experimental,
    'readings': aqs_db.readings
}


def build_search_query(args: dict) -> dict:
    query = {}

    if args['startDate']:
        query["$gte"] = args['startDate']

    if args['endDate']:
        query["$lte"] = args['endDate']

    if not query:
        query["$ne"] = ''

    return query


def insert_doc(document: dict) -> str:
    return aqs_db.AQS.insert_one(document).inserted_id


def insert_many_docs(documents: list, coll: str) -> list:
    return collections[coll].insert_many(documents).inserted_ids


def get_all_docs(coll: str) -> list:
    return list(collections[coll].find())


def find_docs_by_date(date: str) -> list:
    return list(aqs_db.AQS.find({"info.date": f'{date}'}))


# def find_docs_by_name(name: str, date_args: dict) -> list:
#     # rest_api_v1
#     return list(aqs_db.AQS.find({"info.date": build_search_query(date_args), "info.name": f'{name}'}))


def find_docs_by_name(name: str, date_args: dict) -> list:
    # rest_api_v2
    return list(aqs_db.readings.find({"date_debut": build_search_query(date_args), "nom_station": f'{name}'}))


def find_docs_by_area_code(area_code: int, date_args: dict) -> list:
    # rest_api_v2
    return list(aqs_db.readings.find({"date_debut": build_search_query(date_args), "insee_com": area_code}))


def find_docs_by_id(obj_id: str) -> list:
    return list(aqs_db.AQS.find({"_id": ObjectId(obj_id)})) if ObjectId.is_valid(obj_id) else []


def update_docs(docs: list):
    """
    Very time-consuming operation. It will take ~few minutes to complete.
    It can be replaced with function (drop_collection()) which will delete entire collection and create it again,
    but all tracking data (such as last station activity) won't be available.
    """
    bulk_query = [UpdateOne({"name": doc['name']}, {"$set": doc}, upsert=True) for doc in docs]
    aqs_db.stations.bulk_write(bulk_query)


def drop_collection(coll: str) -> bool:
    return collections[coll].drop()


def create_2d_index(coll: str):
    return collections[coll].create_index([("location", GEO2D)])


def create_2dsphere_index(coll: str):
    return collections[coll].create_index([("location", GEOSPHERE)])


def find_near_stations(coll: str, coord: list, min_dist: int = 100, max_dist: int = 10000):
    """
    :param coll: db collection name
    :param coord: coordinates [long, lat] eg. [3.50804, 50.3585]
    :param min_dist: in meters
    :param max_dist: in meters
    :return: list of stations, sorted in order from nearest to farthest
    """

    results = collections[coll].find({
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": coord},
                "$minDistance": min_dist,
                "$maxDistance": max_dist
                }
            }
        })

    return list(results)