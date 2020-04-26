import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import * as jwt_decode from 'jwt-decode';
import { tap } from 'rxjs/operators';
import { Router } from '@angular/router';


@Injectable()
export class JWTInterceptor implements HttpInterceptor {



  constructor(private router: Router) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('token');

    let newHeaders = req.headers;
    if (this.verifyTokenValidate(token)) {
      newHeaders = newHeaders.append('Authorization', `Bearer ${token}`);
    }
    const authReq = req.clone({ headers: newHeaders });
    return next.handle(authReq).pipe(
      tap(() => { }, (err: any) => {
        if (err instanceof HttpErrorResponse) {
          if (err.status !== 401) {
            return this;
          }
          localStorage.removeItem('token');
          this.router.navigate(['/auth']);
        }
      })
    );
  }

  verifyTokenValidate(token) {
    if (token != null) {
      const decoded = jwt_decode(token);
      const currentTime = new Date().getTime() / 1000;
      if (currentTime > decoded.exp) {
        return false;
      } else {
        return true;
      }
    } else {
      return false;
    }
  }
}
