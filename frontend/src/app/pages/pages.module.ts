import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { PagesRoutingModule } from "./pages-routing.module";
import { PagesComponent } from "./pages.component";
import { LayoutModule } from "src/app/layout/layout.module";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatIconModule } from "@angular/material/icon";
import { MatButtonModule } from "@angular/material/button";
import { MatSidenavModule } from "@angular/material/sidenav";
import { MatOptionModule } from "@angular/material/core";
import { SuportComponent } from "./suport/suport.component";
import { SugestionComponent } from "./sugestion/sugestion.component";
import { SidenavglobalService } from "../services/sidenavglobal.service";

@NgModule({
  declarations: [PagesComponent, SuportComponent, SugestionComponent],
  imports: [
    CommonModule,
    MatSidenavModule,
    MatToolbarModule,
    MatOptionModule,
    MatIconModule,
    MatButtonModule,
    PagesRoutingModule,
    LayoutModule
  ],
  providers: [SidenavglobalService],
})
export class PagesModule {}
