import { Component, OnInit, Input } from "@angular/core";
import { Router } from "@angular/router";
import { SidenavComponent } from "../sidenav/sidenav.component";
import { MatSidenav } from "@angular/material/sidenav";
import { SidenavService } from "../sidenav/sidenav.service";

@Component({
  selector: "app-header",
  templateUrl: "./header.component.html",
  styleUrls: ["./header.component.scss"],
})
export class HeaderComponent implements OnInit {
  constructor(private router: Router, private navService: SidenavService) {}

  ngOnInit(): void {}

  toggle() {
    this.navService.openNav();
  }
  sair() {
    localStorage.removeItem("token");
    this.router.navigate(["/"]);
  }
}
