import { Injectable } from '@angular/core';
import {
  CanActivate, CanActivateChild, CanLoad, Route, UrlSegment,
  ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router
} from '@angular/router';
import { Observable } from 'rxjs';
import * as jwt_decode from 'jwt-decode';


@Injectable({
  providedIn: 'root'
})
export class UserGuard implements CanActivate, CanActivateChild, CanLoad {
  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    return this.verifyTokenValidate();

  }
  canActivateChild(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    return this.verifyTokenValidate();
  }
  canLoad(
    route: Route,
    segments: UrlSegment[]): Observable<boolean> | Promise<boolean> | boolean {
    return true;
  }

  verifyTokenValidate() {
    const token = localStorage.getItem('token');



    if (token) {
      const decoded = jwt_decode(token);
      const currentTime = new Date().getTime() / 1000;
      if (currentTime > decoded.exp) {
        this.router.navigate(['/auth']);
        return false;
      } else {
        return true;
      }
    } else {
      this.router.navigate(['/auth']);
      return false;
    }
  }

  constructor(
    private router: Router,
  ) {
  }
}
