# 10.05.2023
# https://data-atmo-hdf.opendata.arcgis.com/datasets/atmo-hdf::mes-hdf-horaire-utd-poll-princ/explore?filters=eyJub21fc3RhdGlvbiI6WyJMaWxsZSBGaXZlcyJdfQ%3D%3D&location=50.151065%2C2.776740%2C9.65&showTable=true

from timeit import default_timer as timer
import pandas as pd

from AQS.aqs_db import insert_many_docs

DROP_NA_ROWS = True


def read_data():
    return pd.read_csv('AQS.csv')


def prepare_data(received_data):
    df = received_data.drop(['X', 'Y', 'metrique', 'x_reg', 'y_reg', 'objectid', 'typologie', 'id_poll_ue', 'ObjectId2'], axis=1)
    today = df.loc[(df['date_debut'] >= '2023/05/09') & (df['date_debut'] < '2023/05/10')]

    if DROP_NA_ROWS:
        today = today.dropna(subset=['valeur'])

    return today.to_dict('records')


def upload_to_db(received_data):
    ids = insert_many_docs(received_data, 'readings')
    print(f'{len(ids)} records added to DB.')


start = timer()

raw_data = read_data()
data = prepare_data(raw_data)
upload_to_db(data)

stop = timer()
print(f'It took: {round((stop - start), 4)} seconds to complete.')
