import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HeaderComponent } from "./header/header.component";
import { SuiModule } from "ng2-semantic-ui";
import { RouterModule } from "@angular/router";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatIconModule } from "@angular/material/icon";
import { MatButtonModule } from "@angular/material/button";
import { SidenavComponent } from "./sidenav/sidenav.component";
import { MatExpansionModule } from "@angular/material/expansion";
import { MatSidenavModule } from "@angular/material/sidenav";
import { SidenavService } from "./sidenav/sidenav.service";
import { MatListModule } from "@angular/material/list";

const COMPONENTS = [HeaderComponent, SidenavComponent];

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
  providers: [SidenavService],
  exports: [COMPONENTS],
})
export class LayoutModule {}
