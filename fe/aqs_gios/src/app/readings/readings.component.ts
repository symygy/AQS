import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { GiosApiService } from '../gios-api.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { ReadingGios } from '../models';


@Component({
  selector: 'app-readings',
  templateUrl: './readings.component.html',
  styleUrls: ['./readings.component.scss']
})
export class ReadingsComponent implements AfterViewInit {
  dataSource: any;
  readings: ReadingGios[] = []
  columns: string[] = ['sensor_id', 'pollutant', 'pollutant_symbol','measurement_date', 'measurement_value'];
  @ViewChild(MatSort) sort!: MatSort;
  pollutants: string[] = []


  constructor(private APIService: GiosApiService, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      if (params['stationCode'] !== undefined) {
        this.getReadings(params['stationCode'])
      }
    })


  }
  ngAfterViewInit(): void {
    this.getReadings()
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  getReadings(code: string = ''){
    this.APIService.getReadings(code).subscribe(
      (readings) => {
        this.readings = readings
        this.dataSource = new MatTableDataSource(readings)
        this.dataSource.sort = this.sort;
    })
  }

  getPollutants(){
    for (let reading of this.readings) {
      if (!this.pollutants.includes(String(reading.pollutant))) {
        this.pollutants.push(String(reading.pollutant))
      }
    }
    return this.pollutants
  }


}
