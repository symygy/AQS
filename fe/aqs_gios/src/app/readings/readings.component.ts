import { Component, ViewChild } from '@angular/core';
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
export class ReadingsComponent {
  dataSource: any;
  readings: ReadingGios[] = []
  columns: string[] = ['sensor_id', 'pollutant', 'pollutant_symbol','measurement_date', 'measurement_value'];
  @ViewChild(MatSort) sort!: MatSort;
  pollutants: string[] = []
  selectedPollutants: string[] = []
  stationCode = ''


  constructor(private APIService: GiosApiService, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      if (params['stationCode'] !== undefined) {
        this.getReadings(params['stationCode'])
        this.stationCode = params['stationCode']
      }
    })
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  getReadings(code: string = ''){
    this.APIService.getReadings(code).subscribe({
      next: (readings) => {
        this.readings = readings

    },
      error: () => {
        this.readings = []
        this.dataSource = new MatTableDataSource(this.readings)
      },
      complete: () => {
        this.dataSource = new MatTableDataSource(this.readings)
        this.dataSource.sort = this.sort;
        this.selectedPollutants = Object.assign([], this.pollutants);
      } 
  
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

  selectPoll(selectedPoll: string) {
    
    if (this.selectedPollutants.includes(selectedPoll)) {
      this.selectedPollutants.splice(this.selectedPollutants.indexOf(selectedPoll, 0), 1)
    } else {
      this.selectedPollutants.push(selectedPoll)
    }
  }

}
