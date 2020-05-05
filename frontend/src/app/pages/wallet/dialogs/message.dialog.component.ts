import { Component, Inject } from "@angular/core";
import { Subscription } from "rxjs";
import { WalletService } from "../services/wallet.service";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { DialogData } from "../wallet.component";

@Component({
  selector: "dialog-mesage",
  template: `
    <h1 mat-dialog-title>{{ data.message }}</h1>

    <div mat-dialog-actions>
      <button (click)="closeDialog()" class="ui button">
        Ok
      </button>
    </div>
  `,
})
export class DialogMessage {
  loading = false;

  constructor(
    private serviceWallet: WalletService,
    public dialogRef: MatDialogRef<DialogMessage>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  closeDialog(data?): void {
    this.dialogRef.close(data);
  }
}
