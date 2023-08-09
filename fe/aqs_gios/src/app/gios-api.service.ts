import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { StationGios, ReadingGios } from './models'

@Injectable({
  providedIn: 'root'
})
export class GiosApiService {

  constructor(private http: HttpClient,) { }

  getStations(): Observable<StationGios[]> {
    return this.http.get<StationGios[]>('http://127.0.0.1:5000/v1/stations/')
  }

  getReadings(station_code: string): Observable<ReadingGios[]> {
    return this.http.get<ReadingGios[]>(`http://127.0.0.1:5000/v1/stations/code/${station_code}`)
  }

  getRange(station_code: string, minDist: string, maxDist: string): Observable<ReadingGios[]> {
    let params = new HttpParams();
    params = params.append('minDist', minDist)
    params = params.append('maxDist', maxDist)
    return this.http.get<ReadingGios[]>(`http://127.0.0.1:5000/v1/stations/range/${station_code}`, {params: params})
    // return this.http.get<ReadingGios[]>(`http://127.0.0.1:5000/v1/stations/range/${station_code}?minDist=${minDist}&maxDist=${maxDist}`)
  }

}
