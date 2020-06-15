import { Component, OnInit, OnDestroy, Inject, ViewChild } from "@angular/core";
import { Subscription } from "rxjs";
import { Wallet } from "src/app/models/wallet.models";
import { MatDialog } from "@angular/material/dialog";
import { WalletService } from "./services/wallet.service";
import { DialogWallet } from "./dialogs/wallet.dialog.component";
import { SidenavglobalService } from "src/app/services/sidenavglobal.service";
import { MatBottomSheet } from "@angular/material/bottom-sheet";
import { BottomSheetComponent } from "./components/bottom-sheet/bottom-sheet.component";
import { PositionWallet, PositionAsset } from "src/app/models/position.models";
import { MatSort } from "@angular/material/sort";
import { MatTableDataSource } from "@angular/material/table";
import { MatPaginator } from "@angular/material/paginator";

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
  walletSelected;

  displayedColumns: string[] = [
    "ticker",
    "quantity",
    "dividends",
    "investments",
    // "costs",
    "index_selic",
    "networth",
  ];

  columnDefs = [
    {
      headerName: "Ticker",
      width: 120,
      field: "ticker",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Quantity",
      width: 120,
      field: "quantity",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Dividends",
      field: "dividends",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Investments",
      field: "investments",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Index Selic",
      field: "index_selic",
      sortable: true,
      filter: true,
    },
    { headerName: "Networth", field: "networth", sortable: true, filter: true },
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
      .getPositionWallet(this.walletSelected)
      .subscribe((data: PositionWallet) => {
        this.positionWallet = data;
      });
  }
}
