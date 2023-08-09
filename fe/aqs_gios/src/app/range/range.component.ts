import { Component, ViewChild } from '@angular/core';
import { GiosApiService } from '../gios-api.service';
import { ActivatedRoute } from '@angular/router';
import { ReadingGios } from '../models';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-range',
  templateUrl: './range.component.html',
  styleUrls: ['./range.component.scss']
})
export class RangeComponent {
  stationCode: string = ''
  minDist: string = '200';
  maxDist: string = '1000';
  dataSource: any;
  readings: ReadingGios[] = []
  columns: string[] = ['station_code', 'station_name', 'sensor_id', 'pollutant', 'pollutant_symbol','measurement_date', 'measurement_value'];
  @ViewChild(MatSort) sort!: MatSort;
  
  rangevalue = '';

  constructor (private APIService: GiosApiService, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      if (params['stationCode'] !== undefined) {
        this.getReadingsInRange(params['stationCode'])
        this.stationCode = params['stationCode']
      }
    })
   }

  getReadingsInRange(stationCode: string, minDist: string='100', maxDist: string='10000') {
    this.APIService.getRange(stationCode, minDist, maxDist).subscribe({
      next: (readings) => {
        this.readings = readings
      },
      error: (e) => {
        this.readings = []
        this.dataSource = new MatTableDataSource(this.readings)
      },
      complete: () => {
        this.dataSource = new MatTableDataSource(this.readings)
        this.dataSource.sort = this.sort;
      }
    }
  )
}

search() {
  console.log(this.minDist, this.maxDist)
  this.getReadingsInRange(this.stationCode, this.minDist, this.maxDist)
}

applyFilter(event: Event) {
  const filterValue = (event.target as HTMLInputElement).value;
  this.dataSource.filter = filterValue.trim().toLowerCase();
}

setMinDist(e: any){
  this.minDist = e.target.value
}

setMaxDist(e: any){
  this.maxDist = e.target.value
}

getMinDist(){
  if (Number(this.minDist) < 1000) return `${this.minDist} m`
  else return `${Number(this.minDist)/1000} km`
}

getMaxDist(){
  if (Number(this.maxDist) < 1000) return `${this.maxDist} m`
  else return `${Number(this.maxDist)/1000} km`
}

}
