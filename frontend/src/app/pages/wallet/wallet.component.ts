import { Component, OnInit, OnDestroy, Inject, ViewChild } from "@angular/core";
import { Subscription } from "rxjs";
import { Wallet } from "src/app/models/wallet.models";
import { MatDialog } from "@angular/material/dialog";
import { WalletService } from "./services/wallet.service";
import { DialogWallet } from "./dialogs/wallet.dialog.component";
import { DialogMessage } from "./dialogs/message.dialog.component";
import { SidenavglobalService } from "src/app/services/sidenavglobal.service";
import { MatBottomSheet } from "@angular/material/bottom-sheet";
import { BottomSheetComponent } from "./components/bottom-sheet/bottom-sheet.component";
import { PositionWallet } from "src/app/models/position.models";
import { MatSort } from "@angular/material/sort";
import { MatTableDataSource } from "@angular/material/table";

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

  displayedColumns: string[] = [
    "acao",
    "quantity",
    "total_investment",
    "total_costs",
    "date",
  ];
  @ViewChild(MatSort, { static: true }) sort: MatSort;
  position: PositionWallet;
  dataSource;

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
        this.dataSource = new MatTableDataSource(data.positions);
      });
  }
}
