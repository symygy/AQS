import { Component, AfterViewInit, ViewChild } from '@angular/core';
import { GiosApiService } from '../gios-api.service';
import { StationGios } from '../models';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';

@Component({
  selector: 'app-stations',
  templateUrl: './stations.component.html',
  styleUrls: ['./stations.component.scss']
})
export class StationsComponent implements AfterViewInit  {
  stations: StationGios[] = []
  columns: string[] = ['station_id', 'station_code', 'station_name', 'city_id', 'city', 'street','voivodeship', 'location', 'data']
  dataSource: any;
  showMap: boolean = false;
  URL: string = ""

  @ViewChild(MatSort) sort!: MatSort;
  
  constructor (private APIService: GiosApiService, public dialog: MatDialog, private router: Router) { }

  ngAfterViewInit(): void {
    this.getStations()
  }

  getStations(){
    this.APIService.getStations().subscribe(
      (stations) => {
        this.stations = stations
        this.dataSource = new MatTableDataSource(stations)
        this.dataSource.sort = this.sort;
    })
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  showLocation(coords: string[]) {
    this.URL =`http://maps.google.com/maps?q=${coords[1]},${coords[0]}&z=16&output=embed`
    this.showMap = !this.showMap
  }

  getData(code: string) {
    this.router.navigate(['/readings'], { queryParams: { stationCode: code } });

  }

}
