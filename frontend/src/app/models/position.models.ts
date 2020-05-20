import { Moviment } from "./moviment.model";

export interface Position {
  total_networth: number;
  total_dividends: number;
  total_invested: number;
  total_selic: number;
  moviments: Moviment[];
}
