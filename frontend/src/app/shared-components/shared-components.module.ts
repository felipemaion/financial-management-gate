import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CampoErrorComponent } from './campo-error/campo-error.component';

const COMPONENTS = [
  CampoErrorComponent
];

@NgModule({
  declarations: COMPONENTS,
  imports: [
    CommonModule
  ],
  exports: [COMPONENTS]
})
export class SharedComponentsModule { }
