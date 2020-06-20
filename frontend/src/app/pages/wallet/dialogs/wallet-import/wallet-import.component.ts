import { Component, OnInit, Inject } from "@angular/core";
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
import { ICellRendererAngularComp } from "ag-grid-angular";
import { MovementService } from "../../services/movement.service";

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
      headerName: "Código",
      field: "instrument",
      width: 130,
      sortable: true,
      filter: true,
      valueGetter: function (params) {
        return params.data.instrument.tckrSymb;
      },
    },
    {
      headerName: "Quantidade",
      width: 120,
      field: "quantity",
      sortable: true,
      filter: true,
    },
    {
      headerName: "Investimento",
      field: "total_investment",
      width: 150,
      sortable: true,
    },
    {
      headerName: "Custos",
      field: "total_costs",
      width: 130,
      sortable: true,
    },
    {
      headerName: "Data",
      field: "date",
      sortable: true,
      width: 120,
      filter: true,
    },
    {
      headerName: "",
      field: "id",
      width: 120,
      cellRendererFramework: ButtomRemoveMovement,
      // onCellClicked: function (params) {
      //   params.api.selectIndex(params.node.rowIndex);
      //   var selectedData = params.api.getSelectedRows();
      //   params.api.updateRowData({remove: selectedData});
      //  }.bind(this)
    },
  ];
  // Table Movements
  gridOptions = {
    rowSelection: "single",
  };

  subscriptions: Subscription = new Subscription();
  walletSelected: Wallet;
  formData: FormData = new FormData();
  loading = false;
  loadingCsv = false;
  loadingMovements = false;
  csvName: string = "Nada Selecionado";
  wallets: Wallet[];
  movements: Moviment[];

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

@Component({
  selector: "app-buttom-remove-movement",
  template: `
    <button (click)="deleteMethod()" aria-label="" style='margin-top: 4px;' class="row-button">
      <mat-icon>delete_forever</mat-icon>
    </button>
    <button aria-label="" class="row-button" style='margin-top: 4px;'>
      <mat-icon>edit</mat-icon>
    </button>
  `,
})
export class ButtomRemoveMovement implements ICellRendererAngularComp {
  public params: any;
  callValue: any;

  constructor(private dialog: MatDialog) {}

  agInit(params: any) {
    this.callValue = params.value;
    this.params = params;
  }

  refresh(params: any) {
    this.callValue = params.value;
    return true;
  }

  public deleteMethod() {
    // this.params.api.selectIndex(this.params.node.rowIndex);
    // var selectedData = this.params.api.getSelectedRows();
    // this.params.api.updateRowData({ remove: selectedData });

    const dialogRef = this.dialog.open(DialogDelete, {
      width: "250px",
      data: { movement: this.callValue },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        if (result.delete) {
          console.log("Deleted");
          this.params.api.selectIndex(this.params.node.rowIndex);
          var selectedData = this.params.api.getSelectedRows();
          this.params.api.updateRowData({ remove: selectedData });
        }
      }
    });
  }
  public editMethod() {
    // this.params.api.setFocusedCell(this.params.node.rowIndex, "courtname");
    // this.params.api.startEditingCell({
    //   rowIndex: this.params.node.rowIndex,
    //   colKey: "courtname",
    // });
  }
}

// Dialog Delete

@Component({
  selector: "dialog-delete",
  templateUrl: "./movement.dialog.html",
})
export class DialogDelete implements OnInit {
  movement;
  loading = false;
  constructor(
    public dialog: MatDialog,
    private movementService: MovementService,
    public dialogRef: MatDialogRef<DialogDelete>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.movement = data;
  }
  ngOnInit() {}

  deleteMovement() {
    this.loading = true;
    this.movementService.removeMovement(this.movement.movement).subscribe(
      (data) => {
        this.loading = false;
        console.log(this.movement);
        this.dialogRef.close({
          delete: true,
        });
      },
      (error) => {
        alert("Error on Delete");
        this.loading = false;
      }
    );
  }
}
