import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header/header.component';
import { SuiModule } from 'ng2-semantic-ui';


const COMPONENTS = [
  HeaderComponent
]



@NgModule({
  declarations: COMPONENTS,
  imports: [
    CommonModule,
    SuiModule
  ],
  exports: [
    COMPONENTS
  ]
})
export class LayoutModule { }
