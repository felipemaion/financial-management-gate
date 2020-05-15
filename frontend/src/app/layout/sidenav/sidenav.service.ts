import { Injectable } from "@angular/core";
import { MatSidenav } from "@angular/material/sidenav";

@Injectable({
  providedIn: "root",
})
export class SidenavService {
  public appDrawer: MatSidenav;

  constructor() {}

  public closeNav() {
    this.appDrawer.close();
  }
  public openNav() {
    console.log("abrindo menu esquerdo");
    this.appDrawer.open();
  }
}
