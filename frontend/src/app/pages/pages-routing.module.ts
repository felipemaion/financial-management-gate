import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { PagesComponent } from "./pages.component";
import { HomeComponent } from "./home/home.component";
import { SugestionComponent } from "./sugestion/sugestion.component";
import { SuportComponent } from "./suport/suport.component";

const routes: Routes = [
  {
    path: "",
    component: PagesComponent,
    children: [
      {
        path: "home",
        component: HomeComponent,
      },
      {
        path: "sugestion",
        component: SugestionComponent,
      },
      {
        path: "suport",
        component: SuportComponent,
      },
      {
        path: "wallets",
        loadChildren: () =>
          import("./wallet/wallet.module").then((m) => m.WalletModule),
      },
      { path: "**", redirectTo: "home" },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PagesRoutingModule {}
