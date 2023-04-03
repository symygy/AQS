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
    data = aqs_db.AQS.find()
    return list(data)

def find_docs_by_date(date: str):
    data = list(aqs_db.AQS.find({ "info.date": f'{date}' }))
    return data or 'No data found'

def find_docs_by_name(name: str):
    data = list(aqs_db.AQS.find({ "info.name": f'{name}' }))
    return data or 'No data found'



# production = client.production # jesli podam nazwe ktora nie istnieje, to zostanie ona utworzona
# person_collection = production.person_collection

