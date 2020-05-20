import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { ExtrasRoutingModule } from "./extras-routing.module";
import { ExtrasComponent } from "./extras.component";
import { MatTabsModule } from "@angular/material/tabs";
import { WalletService } from "../wallet/services/wallet.service";
import { MatDialogModule } from "@angular/material/dialog";
import { MatSelectModule } from "@angular/material/select";
import { FormsModule } from "@angular/forms";

@NgModule({
  declarations: [ExtrasComponent],
  imports: [
    CommonModule,
    MatSelectModule,
    MatDialogModule,
    FormsModule,
    MatTabsModule,
    ExtrasRoutingModule,
  ],
  providers: [WalletService],
})
export class ExtrasModule {}
