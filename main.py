from dotenv import load_dotenv, find_dotenv
from collections import defaultdict
import requests
import json
from aqs_db import insert_many_docs
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


def get_stations_data(data: dict) -> list:
    station_list = []
    for station in data['features']:
        atmo_data = defaultdict(dict)
        _extracted_from_get_stations_data(station, atmo_data, station_list)
    return station_list


def _extracted_from_get_stations_data(station, atmo_data, station_list):
    atmo_data['info']['name'] = station['properties']['lib_zone']
    atmo_data['info']['latitude'] = station['properties']['y_wgs84']
    atmo_data['info']['longitude'] = station['properties']['x_wgs84']
    atmo_data['info']['status'] = station['properties']['code_qual']
    atmo_data['info']['date'] = station['properties']['date_ech']
    atmo_data['atmo']['no2'] = station['properties']['code_no2']
    atmo_data['atmo']['o3'] = station['properties']['code_o3']
    atmo_data['atmo']['pm10'] = station['properties']['code_pm10']
    atmo_data['atmo']['pm25'] = station['properties']['code_pm25']
    atmo_data['atmo']['so2'] = station['properties']['code_so2']

    station_list.append(atmo_data)


if __name__ == '__main__':
    AUTH_HEADER = set_auth_header()

    today_air_data = get_air_qual_info()
    save_resp_to_file(today_air_data)

    air_qual_data = read_resp_from_file()
    get_stations_data(air_qual_data)

    insert_many_docs(get_stations_data(air_qual_data))


