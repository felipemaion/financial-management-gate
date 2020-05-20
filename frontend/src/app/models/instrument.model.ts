export interface Instrument {
  id: number;
  created_at: Date;
  updated_at: Date;
  tckrSymb: string;
  sgmtNm: string;
  mktNm: string;
  sctyCtgyNm: string;
  isin: string;
  cFICd: string;
  crpnNm: string;
  corpGovnLvlNm: string;
  lastUpdate?: any;
}
