import { Component, OnInit, Input } from '@angular/core';
import { Wallet } from "src/app/models/wallet.models";
import { DialogMessage } from "../dialogs/message.dialog.component";
import { Subscription } from "rxjs";
import { WalletService } from "../services/wallet.service";
import { MatDialog } from "@angular/material/dialog";
import { Router, ActivatedRoute } from "@angular/router"

@Component({
  selector: 'app-import',
  templateUrl: './import.component.html',
  styleUrls: ['./import.component.css']
})
export class ImportComponent implements OnInit {
  subscriptions: Subscription = new Subscription();
  // walletSelected; //TODO como não permitir se a carteira não pertencer ao user??
  @Input('wallet') walletSelected;
  formData: FormData = new FormData();
  loadingCsv = false;
  csvName: string = "Nada Selecionado";
  wallets: Wallet[];
  loading = false;
  constructor(private router:Router, private route:ActivatedRoute, public dialog: MatDialog, private walletService: WalletService) { }

  ngOnInit(): void {
    // this.walletSelected = this.route.snapshot.params["wallet"];
    //console.log(this.route.snapshot.params["wallet"]);
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
    this.formData.append("wallet", this.walletSelected);


    this.subscriptions.add(
      this.walletService.sendCsv(this.formData).subscribe(
        (data) => {
          this.loading = false;
          this.dialog.open(DialogMessage, {
            data: { message: "Sucesso Ao Fazer Upload" },
          });
          // this.router.navigate(['wallets']); // Não tá certo TODO.
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
