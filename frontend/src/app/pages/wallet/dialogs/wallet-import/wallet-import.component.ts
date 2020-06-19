import { Component, OnInit, Inject, Input } from "@angular/core";
import {
  MatDialogRef,
  MAT_DIALOG_DATA,
  MatDialog,
} from "@angular/material/dialog";
import { Wallet } from "src/app/models/wallet.models";
import { DialogMessage } from "../message.dialog.component";
import { Subscription } from "rxjs";
import { WalletService } from "../../services/wallet.service";
import { Moviment } from "src/app/models/moviment.model";

export interface DialogData {
  wallet: Wallet;
  name: string;
}

@Component({
  selector: "app-wallet-import",
  templateUrl: "./wallet-import.component.html",
  styleUrls: ["./wallet-import.component.css"],
})
export class WalletImportComponent implements OnInit {
  displayedColumns: string[] = [
    "type",
    "quantity",
    "total_investment",
    "total_costs",
    "date",
    "instrument",
    "created_at",
  ];

  columnDefs = [
    {
      headerName: "instrument",
      field: "instrument",
      sortable: true,
      filter: true,
      valueGetter: function (params) {
        return params.data.instrument.tckrSymb
      },
    },
    {
      headerName: "Quantity",
      width: 120,
      field: "quantity",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Total Investment",
      field: "total_investment",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Total Costs",
      field: "total_costs",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Date",
      field: "date",
      sortable: true,
      filter: true,
    },
  ];
  // Table Movements

  subscriptions: Subscription = new Subscription();
  walletSelected: Wallet;
  formData: FormData = new FormData();
  loadingCsv = false;
  loadingMovements = false;
  csvName: string = "Nada Selecionado";
  wallets: Wallet[];
  movements: Moviment[];
  loading = false;

  constructor(
    public dialog: MatDialog,
    private walletService: WalletService,
    public dialogRef: MatDialogRef<WalletImportComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {
    this.walletSelected = data.wallet;
  }
  ngOnInit(): void {
    this.getMovements();
  }
  onNoClick(): void {
    this.dialogRef.close();
  }

  handleCSVFileInput(event) {
    if (event.length > 0) {
      this.formData.append("file", event[0], event[0].name);
      this.csvName = event[0].name;
    }
  }

  enviarCsv() {
    this.loading = true;
    this.formData.append("wallet", this.walletSelected.id.toString());

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

  getMovements() {
    this.loadingMovements = true;

    this.subscriptions.add(
      this.walletService.getMovements(this.walletSelected.id).subscribe(
        (data) => {
          this.loadingMovements = false;
          this.movements = data;
        },
        (error) => {
          this.loadingMovements = false;
        }
      )
    );
  }
}
