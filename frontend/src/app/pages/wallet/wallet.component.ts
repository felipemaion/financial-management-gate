import { Component, OnInit, OnDestroy, Inject, ViewChild } from "@angular/core";
import { Subscription } from "rxjs";
import { Wallet } from "src/app/models/wallet.models";
import { MatDialog } from "@angular/material/dialog";
import { WalletService } from "./services/wallet.service";
import { DialogWallet } from "./dialogs/wallet.dialog.component";
import { DialogMessage } from "./dialogs/message.dialog.component";
import { SidenavglobalService } from "src/app/services/sidenavglobal.service";

export interface DialogData {
  description: string;
}

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  { position: 1, name: "Hydrogen", weight: 1.0079, symbol: "H" },
  { position: 2, name: "Helium", weight: 4.0026, symbol: "He" },
  { position: 3, name: "Lithium", weight: 6.941, symbol: "Li" },
  { position: 4, name: "Beryllium", weight: 9.0122, symbol: "Be" },
  { position: 5, name: "Boron", weight: 10.811, symbol: "B" },
  { position: 6, name: "Carbon", weight: 12.0107, symbol: "C" },
  { position: 7, name: "Nitrogen", weight: 14.0067, symbol: "N" },
  { position: 8, name: "Oxygen", weight: 15.9994, symbol: "O" },
  { position: 9, name: "Fluorine", weight: 18.9984, symbol: "F" },
  { position: 10, name: "Neon", weight: 20.1797, symbol: "Ne" },
];

@Component({
  selector: "app-wallet",
  templateUrl: "./wallet.component.html",
  styleUrls: ["./wallet.component.css"],
})
export class WalletComponent implements OnInit, OnDestroy {
  subscriptions: Subscription = new Subscription();

  description: string = "";
  carteiras: Wallet[]; // pq em pt?
  loading = false;
  collapse: false;
  carteiraSelected;

  formData: FormData = new FormData();
  loadingCsv = false;
  csvName: string = "Nada Selecionado";

  displayedColumns: string[] = ["position", "name", "weight", "symbol"];
  dataSource = ELEMENT_DATA;

  constructor(
    private walletService: WalletService,
    public dialog: MatDialog,
    private sideGlobalService: SidenavglobalService
  ) {}

  ngOnInit(): void {
    this.getWallets();
  }
  getWallets() {
    this.loading = true;
    this.subscriptions.add(
      this.walletService.getWallets().subscribe(
        (data) => {
          this.carteiras = data;
          this.loading = false;
        },
        (error) => {
          this.loading = false;
        }
      )
    );
  }

  openDialogWallet(): void {
    const dialogRef = this.dialog.open(DialogWallet, {
      width: "250px",
      data: { description: this.description },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.carteiras.push(result);
      }
    });
  }

  handleCSVFileInput(event) {
    console.log(event);
    if (event.length > 0) {
      this.formData.append("file", event[0], event[0].name);
      this.csvName = event[0].name;
    }
  }
  enviarCsv() {
    this.loading = true;
    this.subscriptions.add(
      this.walletService.sendCsv(this.formData).subscribe(
        (data) => {
          this.loading = false;
          this.dialog.open(DialogMessage, {
            data: { message: "Sucesso Ao Fazer Upload" },
          });
        },
        (error) => {
          this.loading = false;
          this.dialog.open(DialogMessage, {
            data: { message: "Error Ao Fazer Upload" },
          });
        }
      )
    );
  }
 
  openGlobalSide() {
    this.sideGlobalService.appDrawer.toggle();
  }
  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }
}
