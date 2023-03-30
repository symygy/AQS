import requests

URL = ''


def login(username: str, password: str):
    body = {
        "username": username,
        "password": password
    }
    return requests.post(URL, data=body)


def get_feeds_list():
    return requests.get(URL)


def get_data_by_id(data_id: int):
    params = {"id": data_id}
    return requests.get(URL, params=params)


def post_data_by_id(data_id: int):
    params = {"id": data_id}
    return requests.post(URL, params=params)


def get_filtered_data_by_id(data_id: int, search: str):
    params = {
        "id": data_id,
        "search": search
    }
    return requests.get(URL, params=params)


def post_filtered_data_by_id(data_id: int, search: str):
    params = {
        "id": data_id,
        "search": search
    }
    return requests.post(URL, params=params)


def get_map_context(context: str):
    params = {
        "context": context,
    }
    return requests.get(URL, params=params)


