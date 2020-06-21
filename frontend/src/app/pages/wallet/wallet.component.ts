import { Component, OnInit, OnDestroy, Inject, ViewChild } from "@angular/core";
import { Subscription } from "rxjs";
import { Wallet } from "src/app/models/wallet.models";
import { MatDialog } from "@angular/material/dialog";
import { WalletService } from "./services/wallet.service";
import { DialogWallet } from "./dialogs/wallet.dialog.component";
import { SidenavglobalService } from "src/app/services/sidenavglobal.service";
import { MatBottomSheet } from "@angular/material/bottom-sheet";
import { BottomSheetComponent } from "./components/bottom-sheet/bottom-sheet.component";
import { PositionWallet } from "src/app/models/position.models";
import { WalletImportComponent } from "./dialogs/wallet-import/wallet-import.component";

export interface DialogData {
  description: string;
}

export interface PeriodicElement {
  acao: string;
  quantity: number;
  total_investment: string;
  total_costs: string;
  date: string;
}

//

export interface UserData {
  id: string;
  name: string;
  progress: string;
  color: string;
}

/** Constants used to fill up our data base. */

@Component({
  selector: "app-wallet",
  templateUrl: "./wallet.component.html",
  styleUrls: ["./wallet.component.css"],
})



export class WalletComponent implements OnInit, OnDestroy {
  subscriptions: Subscription = new Subscription();
  description: string = "";
  wallets: Wallet[];
  loading = false;
  collapse: false;
  walletSelected: Wallet;
  buttonPressed = false;
  
  displayedColumns: string[] = [
    "ticker",
    "quantity",
    "dividends",
    "investments",
    // "costs",
    "index_selic",
    "networth",
  ];

  CurrencyCellRendererBRL(params: any) {
    var inrFormat = new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 2
    });
    return inrFormat.format(params.value);
  }


  columnDefs = [
    {
      headerName: "Código",
      width: 120,
      field: "ticker",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Quantidade",
      width: 120,
      field: "quantity",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Proventos",
      field: "dividends",
      sortable: true,
      filter: true,
      cellRenderer: this.CurrencyCellRendererBRL,
    },
    {
      headerName: "Investimento",
      field: "investments",
      sortable: true,
      filter: true,
      cellRenderer: this.CurrencyCellRendererBRL,
    },
    {
      headerName: "Benchmark SELIC",
      field: "index_selic",
      sortable: true,
      filter: true,
      cellRenderer: this.CurrencyCellRendererBRL,
    },
    { headerName: "Patrimônio", field: "networth", sortable: true, filter: true, cellRenderer: this.CurrencyCellRendererBRL,},
  ];

  positionWallet: PositionWallet;

  constructor(
    private walletService: WalletService,
    public dialog: MatDialog,
    private sideGlobalService: SidenavglobalService,
    private _bottomSheet: MatBottomSheet
  ) {}

  ngOnInit(): void {
    this.getWallets();
  }

  getWallets() {
    this.loading = true;
    this.subscriptions.add(
      this.walletService.getWallets().subscribe(
        (data) => {
          this.wallets = data;
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
        this.wallets.push(result);
      }
    });
  }

  openDialogImport(): void {
    const dialogRef = this.dialog.open(WalletImportComponent, {
      width: "100%",
      data: { wallet: this.walletSelected },
    });

    dialogRef.afterClosed().subscribe((result) => {
      this.getPositionWallet();
    });
  }

  openGlobalSide() {
    this.sideGlobalService.appDrawer.toggle();
  }

  openBalanceBottomSheet() {
    this._bottomSheet.open(BottomSheetComponent, {
      panelClass: "balance-sheet",
    });
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  getPositionWallet() {
    this.walletService
      .getPositionWallet(this.walletSelected.id)
      .subscribe((data: PositionWallet) => {
        this.positionWallet = data;
      });
  }

  change() {
    this.buttonPressed = !this.buttonPressed;
    this.getPositionWallet();
  }
}
