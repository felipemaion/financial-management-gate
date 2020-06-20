import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";
import { HttpClient } from "@angular/common/http";

@Injectable({
  providedIn: "root",
})
export class MovementService {
  api = environment.baseApi;

  constructor(private http: HttpClient) {}

  removeMovement(id: number) {
    return this.http.delete(`${this.api}movement/${id}`);
  }
}
