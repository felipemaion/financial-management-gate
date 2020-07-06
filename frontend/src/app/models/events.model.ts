import { Instrument } from './instrument.model';

export interface Event {
  id: number;
  type: number;
  quantity: number;
  total_investment: string;
  total_costs: string;
  date: string;
  instrument: Instrument;
  created_at: Date;
  updated_at: Date;
}
