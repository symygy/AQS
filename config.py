URL = 'https://admindata.atmo-france.org'
LOGIN = 'mkurek'
PASS = 'AtmoFrance2023'


atmo_schema = {
    'info': {
        'name': str,
        'latitude': str,
        'longitude': str,
        'status': int,
        'date': str
    },
    'atmo': {
        'no2': int,
        'o3': int,
        'pm10': int,
        'pm25': int,
        'so2': int
    }
}
