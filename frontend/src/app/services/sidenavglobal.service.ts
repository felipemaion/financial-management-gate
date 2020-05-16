import { Injectable } from "@angular/core";
import { MatSidenav } from "@angular/material/sidenav";

@Injectable({
  providedIn: "root",
})
export class SidenavglobalService {
  public appDrawer: MatSidenav;

  constructor() {}

  public closeNav() {
    this.appDrawer.close();
  }
  public openNav() {
    console.log("Abrindo Menu Esquerdo");
    this.appDrawer.open();
  }
}
