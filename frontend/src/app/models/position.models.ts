import { Moviment } from "./moviment.model";

export interface PositionWallet {
  total_networth: number;
  total_dividends: number;
  total_invested: number;
  total_selic: number;
  moviments: Moviment[];
  positions: PositionAsset[];
}

export interface PositionAsset {
  ticker:string;
  quantity: number;
  dividends: number;
  investments: number;
  costs: number;
  index_selic: number;
  networth: number;
}
