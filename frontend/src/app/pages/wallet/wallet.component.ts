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
  carteiras: Wallet[]; // pq em pt?
  loading = false;
  collapse: false;
  carteiraSelected;

  displayedColumns: string[] = [
    "ticker",
    "quantity",
    "dividends",
    "investments",
    "costs",
    "index_selic",
    "networth",
  ];
  dataSource: MatTableDataSource<PositionAsset>;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  position: PositionWallet;

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
      .getPositionWallet(this.carteiraSelected)
      .subscribe((data: PositionWallet) => {
        this.position = data;
        this.dataSource = new MatTableDataSource(this.position.positions);
        this.dataSource.paginator = this.paginator;
      });
  }
}
