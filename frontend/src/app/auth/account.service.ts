import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Token } from '../models/token.model';

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  api: string = environment.apiAuth;

  constructor(private http: HttpClient) { }

  login(form: any) {
    return this.http.post<Token>(this.api + 'login', {
      username: form.username,
      password: form.password
    });

  }

  register(form: any) {
    return this.http.post<Token>(this.api + 'register', {
      username: form.username,
      last_name: form.last_name,
      email: form.email,
      password: form.password
    });
  }
}
