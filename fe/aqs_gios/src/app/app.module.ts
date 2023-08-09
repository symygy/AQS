import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { DashboardModule } from './dashboard/dashboard.module';
import { StationsComponent } from './stations/stations.component';
import { StationsModule } from './stations/stations.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ModalModule } from 'ngx-bootstrap/modal';
import { ReadingsComponent } from './readings/readings.component';
import { ReadingsModule } from './readings/readings.module';
import { RangeComponent } from './range/range.component';
import { RangeModule } from './range/range.module';
import { MatIconModule } from '@angular/material/icon';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    DashboardModule,
    StationsModule,
    ReadingsModule,
    MatIconModule,
    RangeModule,
    RouterModule.forRoot([
      {path: '', component: StationsComponent},
      // {path: 'dash', component: DashboardComponent},
      // {path: 'stations', component: StationsComponent},
      {path: 'readings', component: ReadingsComponent},
      {path: 'range', component: RangeComponent},
    ]),
    NgbModule,
    ModalModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
