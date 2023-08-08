import { Component } from '@angular/core';
import { GiosApiService } from '../gios-api.service';
import { StationInfo } from '../models';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent {
  

  constructor (private APIService: GiosApiService) {}

  // getStations(){
  //   this.APIService.getStations().subscribe(
  //     (stations) => {
  //       this.stations = stations
  //   })
  //   console.log(this.stations)
  // }


}
