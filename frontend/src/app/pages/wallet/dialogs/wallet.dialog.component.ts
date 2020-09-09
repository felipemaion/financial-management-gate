import { Component, Inject } from '@angular/core';
import { Subscription } from 'rxjs';
import { WalletService } from '../services/wallet.service';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from '../wallet.component';

@Component({
  selector: "dialog-walle",
  template: `
    <div *ngIf="loading">
      <div class="ui active inverted dimmer">
        <div class="ui large text loader">Loading</div>
      </div>
    </div>

    <h1 mat-dialog-title>Nova Carteira</h1>
    <div mat-dialog-content>
      <div class="">
        <input class="form-control" [(ngModel)]="data.description" placeholder="Nome da Carteira" />
      </div>
    </div>
    <br />
    <div mat-dialog-actions>
      <button (click)="save()" class="btn btn-primary mr-1">
        Salvar
      </button>
      <button (click)="closeDialog()" class="btn btn-primary">
        Cancelar
      </button>
    </div>
  `,
})
export class DialogWallet {
  subscriptions: Subscription = new Subscription();
  loading = false;

  constructor(
    private serviceWallet: WalletService,
    public dialogRef: MatDialogRef<DialogWallet>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  closeDialog(data?): void {
    this.dialogRef.close(data);
  }

  save() {
    this.loading = true;
    this.closeDialog(this.data.description);
    this.subscriptions.add(
      this.serviceWallet.createWallet(this.data.description).subscribe(
        (data) => {
          this.loading = false;
          this.closeDialog(data);
        },
        (error) => {
          this.loading = false;
        }
      )
    );
  }
}
