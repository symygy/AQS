from timeit import default_timer as timer
import requests
import json
import itertools

from AQS.aqs_db import insert_many_docs, drop_collection

FILE_NAME = 'gios_all_stations.csv'
COLLECTION = 'gios'


def get_stations():
    r = requests.get('https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll')
    if r.status_code == 200:
        return json.loads(r.content)["Lista stacji pomiarowych"]


def get_sensors(station_id):
    r = requests.get(f'https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{station_id}')
    if r.status_code == 200:
        return json.loads(r.content)["Lista stanowisk pomiarowych dla podanej stacji"]


def get_data(sensor_id):
    r = requests.get(f'https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/{sensor_id}')
    if r.status_code == 200:
        return json.loads(r.content)["Lista danych pomiarowych"]


def write_data_to_file(data):
    print(f'Writing data to file: {FILE_NAME}...')
    with open(FILE_NAME, 'wb') as csv_file:
        csv_file.write(data)

def prepare_data_record(station_data, sensor_data, reading_data):
    return {
        "Identyfikator stacji": station_data["Identyfikator stacji"],
        "Kod stacji": station_data["Kod stacji"],
        "Nazwa stacji": station_data["Nazwa stacji"],
        "Identyfikator stanowiska": sensor_data["Identyfikator stanowiska"],
        "Wskaźnik": sensor_data["Wskaźnik"],
        "Jednostka": sensor_data["Wskaźnik - wzór"],
        "Data odczytu": reading_data["Data"],
        "Odczyt": reading_data["Wartość"],
        "Lokalizacja": [station_data["WGS84 λ E"], station_data["WGS84 φ N"]]
    }

def upload_to_db(received_data):
    if not received_data:
        print('\nNo data available for specified date')
        exit()
    ids = insert_many_docs(received_data, COLLECTION)
    print(f'\n{len(ids)} records added to DataBase ("{COLLECTION}" collection)')



if __name__=='__main__':

    drop_collection(COLLECTION)

    start = timer()
    stations = get_stations()
    complete_data = []

    for station in stations:
        sensors = get_sensors(station['Identyfikator stacji'])

        for sensor in sensors:
            readings = get_data(sensor['Identyfikator stanowiska'])

            if readings is None:
                continue

            complete_data.extend(prepare_data_record(station, sensor, reading)for reading in readings if reading['Wartość'] is not None)

    upload_to_db(complete_data)

    stop = timer()
    print(f'It took: {round((stop - start), 4)} seconds to complete')




