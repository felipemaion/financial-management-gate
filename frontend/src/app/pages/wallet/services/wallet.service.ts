import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";
import { HttpClient } from "@angular/common/http";
import { Wallet } from "src/app/models/wallet.models";

@Injectable({
  providedIn: "root",
})
export class WalletService {
  api = environment.baseApi;

  constructor(private http: HttpClient) {}

  getWallets() {
    return this.http.get<Wallet[]>(`${this.api}wallet/`);
  }
  createWallet(description) {
    return this.http.post<Wallet>(`${this.api}wallet/`, { description });
  }

  sendCsv(csv) {
    return this.http.post(`${this.api}csv`, csv);
  }
}
