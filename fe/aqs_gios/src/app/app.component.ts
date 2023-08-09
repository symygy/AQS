import { Component, OnInit } from '@angular/core';
import { GiosApiService } from './gios-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'AQS GIOŚ';

  constructor (private router: Router) {}

  getMeHome() {
    this.router.navigate(['']);
  }

}
