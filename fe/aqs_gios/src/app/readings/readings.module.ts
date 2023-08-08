import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReadingsComponent } from './readings.component';
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';

@NgModule({
  declarations: [ReadingsComponent],
  imports: [
    CommonModule,
    MatSortModule,
    MatTableModule,
    MatInputModule,
    MatFormFieldModule,
  ]
})
export class ReadingsModule { }
