import { Component, OnInit, ViewChild, AfterViewInit } from "@angular/core";
import { MatSidenav } from "@angular/material/sidenav";
import { SidenavService } from "./sidenav.service";

@Component({
  selector: "app-sidenav",
  templateUrl: "./sidenav.component.html",
  styleUrls: ["./sidenav.component.scss"],
})
export class SidenavComponent implements OnInit, AfterViewInit {
  @ViewChild("drawer") drawer: MatSidenav;

  constructor(private navService: SidenavService) {}

  ngAfterViewInit() {
    this.navService.appDrawer = this.drawer
  }
  toggle() {
    this.drawer.toggle();
  }

  ngOnInit(): void {}
}
