import requests
import json
from config import *



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
    return json.loads(r.content)


def get_data_by_id(data_id: int):
    params = {"withGeom": "false"}

    # r = requests.get(f'{URL}/api/data/{data_id}', params=params, headers=AUTH_HEADER)
    r = requests.head(f'{URL}/api/data/{data_id}')
    print(r.headers)
    # return json.loads(r.content)


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




if __name__ == '__main__':
    AUTH_HEADER = set_auth_header()
    # print(json.dumps(get_data_by_id(113), indent=4))

    print(json.dumps(get_feeds_list(), indent=4))
