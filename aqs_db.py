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


def find_docs_by_name(name: str):
    return list(aqs_db.AQS.find({"info.name": f'{name}'}))


def find_docs_by_id(obj_id: str):
    if not ObjectId.is_valid(obj_id):
        return []

    return list(aqs_db.AQS.find({"_id": ObjectId(obj_id)}))


def find_docs_by_date_range(start_date: str, end_date: str, name: str):
    return list(aqs_db.AQS.find({"info.date": {"$gt": f'{start_date}', "$lt": f'{end_date}'}, 'info.name':f'{name}'}))

