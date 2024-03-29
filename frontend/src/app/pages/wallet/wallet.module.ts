import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { CommonModule } from "@angular/common";

import { WalletRoutingModule } from "./wallet-routing.module";
import { WalletComponent } from "./wallet.component";
import { FormsModule } from "@angular/forms";
import { MatSelectModule } from "@angular/material/select";
import { WalletService } from "./services/wallet.service";
import { MatDialogModule } from "@angular/material/dialog";
import { DialogWallet } from "./dialogs/wallet.dialog.component";
import { MatTabsModule } from "@angular/material/tabs";
import { MatTableModule } from "@angular/material/table";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatIconModule } from "@angular/material/icon";
import { MatButtonModule } from "@angular/material/button";
import { MatBottomSheetModule } from "@angular/material/bottom-sheet";
import { BottomSheetComponent } from "./components/bottom-sheet/bottom-sheet.component";
import { MatGridListModule } from "@angular/material/grid-list";
import { MatExpansionModule } from "@angular/material/expansion";
import { MatListModule } from "@angular/material/list";
import { MatSortModule } from "@angular/material/sort";
import { MatPaginatorModule } from "@angular/material/paginator";
import { ImportComponent } from "./import/import.component";
import { AgGridModule } from "ag-grid-angular";
import {
  WalletImportComponent,
  ButtomRemoveMovement,
  DialogDelete,
} from "./dialogs/wallet-import/wallet-import.component";
import { MovementService } from "./services/movement.service";

@NgModule({
  declarations: [
    WalletComponent,
    ButtomRemoveMovement,
    DialogDelete,
    WalletImportComponent,
    DialogWallet,
    BottomSheetComponent,
    ImportComponent,
    WalletImportComponent,
  ],
  imports: [
    CommonModule,
    MatSelectModule,
    MatTabsModule,
    MatTableModule,
    MatButtonModule,
    MatToolbarModule,
    FormsModule,
    MatIconModule,
    WalletRoutingModule,
    MatExpansionModule,
    MatDialogModule,
    MatListModule,
    MatBottomSheetModule,
    MatGridListModule,
    MatSortModule,
    MatPaginatorModule,
    AgGridModule.withComponents([]),
  ],
  providers: [WalletService, MovementService],
  entryComponents: [BottomSheetComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class WalletModule {}
