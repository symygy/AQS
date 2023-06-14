# ATMO HAUTS-DE-FRANCE
# https://data-atmo-hdf.opendata.arcgis.com/datasets/atmo-hdf::mes-hdf-horaire-utd-poll-princ/explore?location=50.140867%2C2.776740%2C9.67
import json
import time
from timeit import default_timer as timer
from datetime import datetime, timedelta
import pandas as pd
import requests
import os
from AQS.aqs_db import insert_many_docs, drop_collection, create_2d_index, create_2dsphere_index, find_near_stations

UPDATE_DATA_URL = "https://opendata.arcgis.com/api/v3/datasets/260a8f0eee5c4dcba12070ee1a8cb4d5_0/downloads"
UPDATE_DATA_BODY = {"spatialRefId":"{\"wkid\":102100,\"latestWkid\":3857}","format":"csv","where":"1=1"}
DOWNLOAD_DATA_URL = "https://opendata.arcgis.com/api/v3/datasets/260a8f0eee5c4dcba12070ee1a8cb4d5_0/downloads/data?format=csv&spatialRefId=3857&where=1=1"

FILE_NAME = 'AQS.csv'
COLLECTION = 'readings'
DROP_NA_ROWS = True # defines if rows with empty values will be dropped or not
RETRIES = 20


def request_update_data():
    print('Requesting data file update...')
    return requests.post(UPDATE_DATA_URL, json=UPDATE_DATA_BODY)

def request_download_data():
    print('Requesting data file download...')
    return requests.get(DOWNLOAD_DATA_URL)

def download_data():
    retries = RETRIES
    while retries:
        r = request_update_data()
        r_json = json.loads(r.content)

        print(f"Attempting to download the data... Remaining attempts: {retries-1}")

        if r.status_code != 202 or "job" in r_json["attributes"]:
            time.sleep(10)
            retries -= 1
            continue
        break

    if not retries:
        print(f"\nCouldn't download data in {RETRIES} attempts")
        exit()

    return request_download_data()

def write_data_to_file():
    atmo_data = download_data()

    if atmo_data.status_code != 200:
        print(f'Downloading data failed... Status code: {atmo_data.status_code}')
        exit()

    print(f'Writing data to file: {FILE_NAME}...')
    with open(FILE_NAME, 'wb') as csv_file:
        csv_file.write(atmo_data.content)

def read_data():
    print(f"Reading data from file: {FILE_NAME}...")
    file_path = f'{os.getcwd()}/{FILE_NAME}'
    if not os.path.isfile(file_path):
        print(f'No {FILE_NAME} file found')
        exit()

    return pd.read_csv('AQS.csv')

def get_current_date():
    return datetime.now().strftime('%Y/%m/%d')

def get_tomorrow_date():
    return (datetime.now() + timedelta(days=1)).strftime('%Y/%m/%d')

def prepare_data(received_data):
    df = received_data
    df['location'] = df[['x_wgs84', 'y_wgs84']].values.tolist()
    df = df.drop(['X', 'Y', 'metrique', 'x_reg', 'y_reg', 'objectid', 'typologie', 'id_poll_ue', 'ObjectId2', 'y_wgs84', 'x_wgs84'], axis=1)
    # df_today = df.loc[(df['date_debut'] >= '2023/06/05') & (df['date_debut'] < '2023/06/06')]
    df_today = df.loc[(df['date_debut'] >= get_current_date()) & (df['date_debut'] < get_tomorrow_date())]

    if DROP_NA_ROWS:
        df_today = df_today.dropna(subset=['valeur'])

    return df_today.to_dict('records')

def upload_to_db(received_data):
    if not received_data:
        print('\nNo data available for specified date')
        exit()
    ids = insert_many_docs(received_data, COLLECTION)
    print(f'\n{len(ids)} records added to DataBase ("{COLLECTION}" collection)')


# drop_collection(COLLECTION) # to delete

start = timer()

# write_data_to_file()
raw_data = read_data()
data = prepare_data(raw_data)
upload_to_db(data)

# create_2dsphere_index(COLLECTION)

# print(len(find_near_stations(COLLECTION, [3.50804, 50.3585], 100, 1300)))

stop = timer()
print(f'It took: {round((stop - start), 4)} seconds to complete')
