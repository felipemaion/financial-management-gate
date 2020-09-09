import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as jwt_decode from 'jwt-decode';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { AccountService } from '../account.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {



  subscriptions: Subscription = new Subscription();
  form: FormGroup;
  loading = false;
  isLogged = false;
  errors;




  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private accountService: AccountService

  ) {
    this.form = this.formBuilder.group({
      username: ['', [Validators.minLength(3), Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  ngOnInit() {
    this.verifyTokenValidate();
  }

  logar() {
    const router = this.router;
    const asyncLocalStorage = {
      setItem: (key, value) => {
        return Promise.resolve().then(() => {
          localStorage.setItem(key, value);
        });
      },
      getItem: (key) => {
        return Promise.resolve().then(() => {
          return localStorage.getItem(key);
        });
      }
    };

    this.errors = null;
    this.loading = true;
    if (this.form.valid) {
      this.subscriptions.add(
        this.accountService.login(this.form.value).subscribe(
          data => {
            this.isLogged = true;
            asyncLocalStorage.setItem('token', data.token).then(() => {
              return asyncLocalStorage.getItem('token').then((value) => {
                setTimeout(() => {
                  router.navigate(['/user']);
                }, 2000);
              });
            });
          },
          error => {
            this.errors = error;
            this.loading = false;
          }
        )
      );
    } else {
      Object.keys(this.form.controls).forEach(campo => {
        const controle = this.form.get(campo);
        controle.markAsTouched();
      });
      this.loading = false;
    }
  }




  verifyTokenValidate() {
    const token = localStorage.getItem('token');
    if (token) {
      const decoded = jwt_decode(token);
      const currentTime = new Date().getTime() / 1000;
      if (currentTime > decoded.exp) {
        return false;
      } else {
        this.router.navigate(['/user']);
        return true;
      }
    }
  }

  verificaValidTouched(campo) {
    return !this.form.get(campo).valid && this.form.get(campo).touched;
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }
}
