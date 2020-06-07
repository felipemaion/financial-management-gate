import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { WalletComponent } from './wallet.component';
import { ImportComponent } from './import/import.component'

const routes: Routes = [
  {
    path: '',
    component: WalletComponent
  },
  {
    path:'import/:wallet',
    component:ImportComponent  // Cria esse componente pra 
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WalletRoutingModule { }
