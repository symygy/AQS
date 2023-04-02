from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())

password = os.environ.get('MONGODB_PWD')

connection_str = f'mongodb+srv://mkurek:{password}@aqs.bsjlrtb.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(connection_str)

dbs = client.list_database_names()

aqs_db = client.AQS
collections = aqs_db.list_collection_names()


def insert_doc(document: dict):
    collection = aqs_db.AQS
    inserted_id = collection.insert_one(document).inserted_id
    print(inserted_id)


def insert_many_docs(documents: list):
    collection = aqs_db.AQS
    inserted_ids = collection.insert_many(documents).inserted_ids
    print(f"{len(inserted_ids)} documents successfully inserted to DB")

# production = client.production # jesli podam nazwe ktora nie istnieje, to zostanie ona utworzona
# person_collection = production.person_collection

