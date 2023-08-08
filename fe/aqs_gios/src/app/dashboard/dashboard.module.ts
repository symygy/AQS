import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { DashboardComponent } from './dashboard.component';



@NgModule({
  imports: [
    CommonModule,
    MatCardModule, 
    MatButtonModule
  ],
  declarations: [DashboardComponent],
})
export class DashboardModule { }
