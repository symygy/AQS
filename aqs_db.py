from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

load_dotenv(find_dotenv())
password = os.environ.get('PASS')

connection_str = f'mongodb+srv://mkurek:{password}@aqs.bsjlrtb.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(connection_str)

dbs = client.list_database_names()

aqs_db = client.AQS
collections = aqs_db.list_collection_names()


def build_search_query(args: dict):
    query = {}

    if args['startDate']:
        query["$gte"] = args['startDate']

    if args['endDate']:
        query["$lte"] = args['endDate']

    if not query:
        query["$ne"] = ''

    return query


def insert_doc(document: dict):
    inserted_id = aqs_db.AQS.insert_one(document).inserted_id
    print(inserted_id)


def insert_many_docs(documents: list):
    inserted_ids = aqs_db.AQS.insert_many(documents).inserted_ids
    print(f"{len(inserted_ids)} documents were successfully inserted to DB")


def get_all_docs():
    return list(aqs_db.AQS.find())


def find_docs_by_date(date: str):
    return list(aqs_db.AQS.find({"info.date": f'{date}'}))


def find_docs_by_name(name: str, date_args: dict):
    return list(aqs_db.AQS.find({"info.date": build_search_query(date_args), "info.name": f'{name}'}))


def find_docs_by_id(obj_id: str):
    return list(aqs_db.AQS.find({"_id": ObjectId(obj_id)})) if ObjectId.is_valid(obj_id) else []



