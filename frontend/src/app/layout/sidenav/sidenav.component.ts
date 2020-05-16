import { Component, OnInit, ViewChild, AfterViewInit } from "@angular/core";
import { MatSidenav } from "@angular/material/sidenav";
import { SidenavglobalService } from "src/app/services/sidenavglobal.service";

@Component({
  selector: "app-sidenav",
  templateUrl: "./sidenav.component.html",
  styleUrls: ["./sidenav.component.scss"],
})
export class SidenavComponent implements OnInit, AfterViewInit {
  @ViewChild("drawer") drawer: MatSidenav;

  constructor(private navService: SidenavglobalService) {}

  ngAfterViewInit() {
    this.navService.appDrawer = this.drawer;
  }
  toggle() {
    this.navService.closeNav();
  }

  ngOnInit(): void {}
}
