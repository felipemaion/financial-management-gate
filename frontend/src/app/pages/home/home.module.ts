import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { MatSidenavModule } from "@angular/material/sidenav";
import { HomeComponent } from "./home.component";
import { MatIconModule } from "@angular/material/icon";
import { HomeRoutingModule } from "./home.routing.module";

@NgModule({
  declarations: [HomeComponent],
  imports: [CommonModule, HomeRoutingModule, MatSidenavModule, MatIconModule],
})
export class HomeModule {}
