import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { WalletRoutingModule } from './wallet-routing.module';
import { WalletComponent, DialogOverviewExampleDialog } from './wallet.component';
import { FormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { WalletService } from './services/wallet.service';
import { MatDialogModule } from '@angular/material/dialog';




@NgModule({
  declarations: [
    WalletComponent,
    DialogOverviewExampleDialog
  ],
  imports: [
    CommonModule,
    MatSelectModule,
    FormsModule,
    WalletRoutingModule,
    MatDialogModule
  ],
  providers: [
    WalletService
  ]
})
export class WalletModule { }
