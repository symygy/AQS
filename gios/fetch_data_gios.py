from timeit import default_timer as timer
import requests
import json
from AQS.gios.aqs_db import insert_many_docs, drop_collection, create_2dsphere_index

FILE_NAME = '../gios_all_stations.csv'
COLLECTION = 'gios'

def get_stations():
    """ Returns all atmo stations from GIOŚ """
    r = requests.get('https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll')
    if r.status_code == 200:
        return json.loads(r.content)["Lista stacji pomiarowych"]


def get_sensors(station_id):
    """ Returns all sensors related to station """
    r = requests.get(f'https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{station_id}')
    if r.status_code == 200:
        return json.loads(r.content)["Lista stanowisk pomiarowych dla podanej stacji"]


def get_data(sensor_id):
    """ Returns sensors related data"""
    r = requests.get(f'https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/{sensor_id}')
    if r.status_code == 200:
        return json.loads(r.content)["Lista danych pomiarowych"]


def prepare_data_record(station_data, sensor_data, reading_data):
    """ Returns single data record """
    return {
        "station_id": station_data["Identyfikator stacji"],
        "station_code": station_data["Kod stacji"],
        "station_name": station_data["Nazwa stacji"],
        "sensor_id": sensor_data["Identyfikator stanowiska"],
        "pollutant": sensor_data["Wskaźnik"],
        "pollutant_symbol": sensor_data["Wskaźnik - wzór"],
        "measurement_date": reading_data["Data"],
        "measurement_value": reading_data["Wartość"],
        "location": [float(station_data["WGS84 λ E"]), float(station_data["WGS84 φ N"])]
    }

def upload_to_db(received_data):
    """ Uploads list of data records to db """
    if not received_data:
        exit()
    ids = insert_many_docs(received_data)
    print(f'\n{len(ids)} records added to DataBase ("{COLLECTION}" collection)')



if __name__=='__main__':

    # drop_collection()

    start = timer()

    print("Fetching atmo data...")
    stations = get_stations()
    complete_data = []

    for station in stations:
        sensors = get_sensors(station['Identyfikator stacji'])

        for sensor in sensors:
            readings = get_data(sensor['Identyfikator stanowiska'])

            if readings is None:
                continue

            complete_data.extend(prepare_data_record(station, sensor, reading) for reading in readings if reading['Wartość'] is not None)

    print("Uploading data to db...")
    upload_to_db(complete_data)

    create_2dsphere_index()

    stop = timer()
    print(f'It took: {round((stop - start), 4)} seconds to complete')




