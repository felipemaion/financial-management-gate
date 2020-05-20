import { Component, OnInit } from "@angular/core";
import { Wallet } from "src/app/models/wallet.models";
import { Subscription } from "rxjs";
import { WalletService } from "../wallet/services/wallet.service";
import { MatDialog } from "@angular/material/dialog";
import { DialogMessage } from "../wallet/dialogs/message.dialog.component";

@Component({
  selector: "app-extras",
  templateUrl: "./extras.component.html",
  styleUrls: ["./extras.component.css"],
})
export class ExtrasComponent implements OnInit {
  subscriptions: Subscription = new Subscription();

  formData: FormData = new FormData();
  loadingCsv = false;
  csvName: string = "Nada Selecionado";
  carteiraSelected;
  carteiras: Wallet[];
  loading = false;

  constructor(public dialog: MatDialog, private walletService: WalletService) {}

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
}
