export class StationGios {
    _id?: number;
    station_id?: number;
    station_code?: string;
    station_name?: string;
    city_id?: number;
    city?: string;
    community?: string;
    county?: string;
    voivodeship?: string;
    street?: string;
    location?: [];
}

export class ReadingGios {
    _id?: number;
    station_id?: number;
    station_code?: string;
    station_name?: string;
    sensor_id?: number;
    pollutant?: string;
    pollutant_symbol?: string;
    measurement_date?: string;
    measurement_value?: number;
}

export class StationInfo {
    _id?: string;
    station_id?: number;
    station_code?: string;
    station_name?: string;
    sensor_id?: number;
    pollutant?: string;
    pollutant_symbol?: string;
    measurement_date?: string;
    measurement_value?: number;
    location?: string[]
}


