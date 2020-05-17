import { Component, OnInit, ViewChild, AfterViewInit } from "@angular/core";
import { MatSidenav } from "@angular/material/sidenav";
import { SidenavglobalService } from "../services/sidenavglobal.service";

@Component({
  selector: "app-pages",
  templateUrl: "./pages.component.html",
  styleUrls: ["./pages.component.css"],
})
export class PagesComponent implements OnInit, AfterViewInit {
  @ViewChild("drawer") drawer: MatSidenav;

  constructor(private navService: SidenavglobalService) {}

  ngAfterViewInit() {
    this.navService.appDrawer = this.drawer;
  }

  ngOnInit(): void {}
}
