import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";
import { HttpClient } from "@angular/common/http";
import { Wallet } from "src/app/models/wallet.models";
import { PositionWallet } from "src/app/models/position.models";
import { Moviment } from 'src/app/models/moviment.model';

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

  getPositionWallet(walletId: number) {
    return this.http.get<PositionWallet>(`${this.api}position/${walletId}`);
  }
  getMovements(walletId:number){
    return this.http.get<Moviment[]>(`${this.api}wallet/${walletId}/movements`);
  }
}
