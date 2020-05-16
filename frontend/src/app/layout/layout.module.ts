import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HeaderComponent } from "./header/header.component";
import { SuiModule } from "ng2-semantic-ui";
import { RouterModule } from "@angular/router";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatIconModule } from "@angular/material/icon";
import { MatButtonModule } from "@angular/material/button";
import { MatExpansionModule } from "@angular/material/expansion";
import { MatSidenavModule } from "@angular/material/sidenav";

import { MatListModule } from "@angular/material/list";
import { SidenavglobalService } from "../services/sidenavglobal.service";
import { SideNavContentComponent } from "./sidenav-content/sidenav-content.component";
import { MatBottomSheetModule } from "@angular/material/bottom-sheet";

const COMPONENTS = [HeaderComponent, SideNavContentComponent];

@NgModule({
  declarations: COMPONENTS,
  imports: [
    CommonModule,
    MatSidenavModule,
    MatButtonModule,
    MatIconModule,
    MatExpansionModule,
    MatToolbarModule,
    SuiModule,
    MatListModule,
    RouterModule,
  ],
  providers: [SidenavglobalService],
  exports: [COMPONENTS, MatSidenavModule],
  
})
export class LayoutModule {}
