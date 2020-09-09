import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { AuthComponent } from './auth.component';
import { AuthRoutingModule } from './auth-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AccountService } from './account.service';
import { SharedComponentsModule } from '../shared-components/shared-components.module';
import { AlertModule } from 'ngx-bootstrap/alert';



@NgModule({
  declarations: [
    LoginComponent,
    RegisterComponent,
    AuthComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    AuthRoutingModule,
    SharedComponentsModule,
    AlertModule.forRoot(),
  ],
  providers: [
    AccountService
  ]
})
export class AuthModule { }
