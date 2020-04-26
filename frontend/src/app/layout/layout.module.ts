import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header/header.component';
import { SuiModule } from 'ng2-semantic-ui';
import { RouterModule } from '@angular/router';


const COMPONENTS = [
  HeaderComponent
]



@NgModule({
  declarations: COMPONENTS,
  imports: [
    CommonModule,
    SuiModule,
    RouterModule
  ],
  exports: [
    COMPONENTS
  ]
})
export class LayoutModule { }
