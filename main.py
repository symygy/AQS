from dotenv import load_dotenv, find_dotenv
from collections import defaultdict
import requests
import json
from aqs_db import get_all_docs, find_docs_by_date, find_docs_by_name, insert_many_docs, update_docs, drop_collection
from datetime import date
import os

load_dotenv(find_dotenv())
LOGIN = os.environ.get('LOGIN')
PASS = os.environ.get('PASS')
URL = os.environ.get('URL')


def get_JWT():
    body = {
        "username": LOGIN,
        "password": PASS
    }
    r = requests.post(f'{URL}/api/login', json=body)
    return json.loads(r.content)["token"]


def set_auth_header():
    return {'Authorization': f'Bearer {get_JWT()}'}


def get_feeds_list():
    r = requests.get(f'{URL}/api/feeds', headers=AUTH_HEADER)
    return r.content


def get_data_by_id(data_id: int = 113, query: str = None):
    data = f'{data_id}/{query}' if query else data_id

    r = requests.get(f'{URL}/api/data/{data}', headers=AUTH_HEADER)
    return r.content


def get_data_by_id_with_date(date: str):
    get_data_by_id()


def post_data_by_id(data_id: int):
    params = {"id": data_id}
    return requests.post(URL, params=params, headers=AUTH_HEADER)


def get_filtered_data_by_id(data_id: int, search: str):
    params = {
        "id": data_id,
        "search": search
    }
    return requests.get(URL, params=params, headers=AUTH_HEADER)


def post_filtered_data_by_id(data_id: int, search: str):
    params = {
        "id": data_id,
        "search": search
    }
    return requests.post(URL, params=params, headers=AUTH_HEADER)


def get_map_context(context: str):
    params = {
        "context": context,
    }
    return requests.get(URL, params=params, headers=AUTH_HEADER)


##
def get_current_date():
    return str(date.today())


def get_air_qual_info(curr_date: str = get_current_date()):
    query = '{"date_ech":{"operator":"=","value":' + f'"{curr_date}"' + '}}'
    return get_data_by_id(112, query)


def save_resp_to_file(resp, filename: str = 'resp.json'):
    with open(filename, 'wb') as f:
        f.write(resp)


def read_resp_from_file(filename: str = 'resp.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def get_atmo_data(data: dict) -> list:
    station_list = []
    for entry in data['features']:
        atmo_data = defaultdict(dict)
        _extracted_from_get_atmo_data(entry, atmo_data, station_list)
    return station_list


def get_station_list(data: dict) -> list:
    station_list = []
    for entry in data['features']:
        station_data = defaultdict(dict)
        _extracted_from_get_station_list(entry, station_data, station_list)

    return station_list


def _extracted_from_get_atmo_data(entry, atmo_data, station_list):
    atmo_data['info']['name'] = entry['properties']['lib_zone']
    atmo_data['info']['latitude'] = entry['properties']['y_wgs84']
    atmo_data['info']['longitude'] = entry['properties']['x_wgs84']
    atmo_data['info']['status'] = entry['properties']['code_qual']
    atmo_data['info']['date'] = entry['properties']['date_ech']
    atmo_data['atmo']['no2'] = entry['properties']['code_no2']
    atmo_data['atmo']['o3'] = entry['properties']['code_o3']
    atmo_data['atmo']['pm10'] = entry['properties']['code_pm10']
    atmo_data['atmo']['pm25'] = entry['properties']['code_pm25']
    atmo_data['atmo']['so2'] = entry['properties']['code_so2']

    station_list.append(atmo_data)


def _extracted_from_get_station_list(entry, station_data, station_list):
    station_data['name'] = entry['properties']['lib_zone']
    station_data['latitude'] = entry['properties']['y_wgs84']
    station_data['longitude'] = entry['properties']['x_wgs84']
    station_data['status'] = entry['properties']['code_qual']

    station_list.append(station_data)


def update_stations_collection(station_list: list):
    inserted_ids = insert_many_docs(station_list, 'stations')
    print(f"{len(inserted_ids)} documents were successfully inserted to stations collection")


def update_atmo_collection(atmo_data_list: list):
    inserted_ids = insert_many_docs(atmo_data_list, 'atmo')
    print(f"{len(inserted_ids)} documents were successfully inserted to AQS collection")


def delete_stations_collection():
    print('Collection stations will be dropped if exists')
    return drop_collection('stations')


if __name__ == '__main__':
    AUTH_HEADER = set_auth_header()

    # today_air_data = get_air_qual_info()
    # save_resp_to_file(today_air_data)

    air_qual_data = read_resp_from_file()

    # delete_stations_collection()
    # update_stations_collection(get_station_list(air_qual_data))

    update_atmo_collection(get_atmo_data(air_qual_data))
    # update_stations_collection(get_station_list(air_qual_data))
