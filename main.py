import requests
import json
from config import *

QUALITY_COL_NAMES = ['lib_zone', 'lib_qual', 'code_qual', 'code_no2', 'code_o3', 'code_pm10', 'code_pm25', 'code_so2',
                     'y_wgs84', 'x_wgs84']


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
def get_air_qual_info(date: str = '2023-01-16'):
    query = '{"date_ech":{"operator":"=","value":' + f'"{date}"' + '}}'
    return get_data_by_id(112, query)


def save_resp_to_file(resp, filename: str = 'resp.json'):
    with open(filename, 'wb', encoding='utf-8') as f:
        f.write(resp)


def read_resp_from_file(filename: str = 'resp.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def get_pretty_unit_data(data: dict) -> dict:
    atmo_data = atmo_schema.copy()

    atmo_data['info']['name'] = data['lib_zone']
    atmo_data['info']['latitude'] = data['y_wgs84']
    atmo_data['info']['longitude'] = data['x_wgs84']
    atmo_data['info']['status'] = data['code_qual']
    atmo_data['atmo']['no2'] = data['code_no2']
    atmo_data['atmo']['o3'] = data['code_o3']
    atmo_data['atmo']['pm10'] = data['code_pm10']
    atmo_data['atmo']['pm25'] = data['code_pm25']
    atmo_data['atmo']['so2'] = data['code_so2']

    return atmo_data


if __name__ == '__main__':
    AUTH_HEADER = set_auth_header()

    # air_qual_data = get_air_qual_info()
    # save_resp_to_file(air_qual_data)

    air_qual_data = read_resp_from_file()

    for unit in air_qual_data['features']:
        print(get_pretty_unit_data(unit['properties']))
