import { Component, OnInit, OnDestroy, Inject } from '@angular/core';
import { Subscription } from 'rxjs';
import { Wallet } from 'src/app/models/wallet.models';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { WalletService } from './services/wallet.service';

export interface DialogData {
  description: string;
}

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.css']
})
export class WalletComponent implements OnInit, OnDestroy {

  subscriptions: Subscription = new Subscription();
  description: string = '';
  carteiras: Wallet[]; // pq em pt?
  loading = false;
  collapse: false;
  constructor(private walletService: WalletService, public dialog: MatDialog) { 

  }

  ngOnInit(): void {
    this.getWallets();
  }
  getWallets() {
    this.loading = true
    this.subscriptions.add(
      this.walletService.getWallets().subscribe(
        data => {
          this.carteiras = data;
          this.loading = false;

        }, error => {
          this.loading = false;
        }
      )
    )
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '250px',
      data: { description: this.description }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.carteiras.push(result);
      }
    });
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }
}


@Component({
  selector: 'dialog-overview-example-dialog',
  template: `

  <div *ngIf="loading" >
    <div class="ui active inverted dimmer">
    <div class="ui large text loader">Loading</div>
    </div>
  </div>


    <h1 mat-dialog-title>Nova Carteira </h1>
    <div mat-dialog-content>
      <div class="ui fluid input">
        <input [(ngModel)]="data.description" placeholder="Nome da Carteira">
      </div> 
    </div> 
    <br>
    <div mat-dialog-actions>
      <button (click)="save()" class="ui button">
      Salvar
      </button>
        <button (click)="closeDialog()" class="ui button">
        Cancelar
        </button>

    </div>
  `,

})
export class DialogOverviewExampleDialog {
  subscriptions: Subscription = new Subscription();
  loading = false;

  constructor(
    private serviceWallet: WalletService,
    public dialogRef: MatDialogRef<DialogOverviewExampleDialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) { }

  closeDialog(data?): void {
    this.dialogRef.close(
      data
    );
  }

  save() {
    this.loading = true;
    this.closeDialog(this.data.description);
    this.subscriptions.add(
      this.serviceWallet.createWallet(this.data.description).subscribe(
        data => {
          this.loading = false;
          this.closeDialog(data);
        },
        error => {
          this.loading = false;
        }
      )

    )
  }
}