import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AccountService } from '../account.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

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
      email: ['', [Validators.email]],
      password: ['', [Validators.minLength(3), Validators.required]],
    });
  }
  ngOnInit(): void {
  }

  verificaValidTouched(campo) {
    return !this.form.get(campo).valid && this.form.get(campo).touched;
  }
  registrar() {
    this.errors = null;
    this.loading = true;
    if (this.form.valid) {
      this.subscriptions.add(
        this.accountService.register(this.form.value).subscribe(
          data => {
            this.isLogged = true;
            localStorage.setItem('token', data.token);
            setTimeout(() => {
              this.router.navigate(['/user']);
            }, 2000);
          },
          error => {
            this.errors = error;
            this.loading = false;
          }
        )
      );
    } else {
      this.loading = false;
      Object.keys(this.form.controls).forEach(campo => {
        const controle = this.form.get(campo);
        controle.markAsTouched();
      });
    }
  }
}
