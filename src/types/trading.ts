/**
 * Shared trading domain types used across the ANGEL.AI web application.
 */
export type OrderSide = 'BUY' | 'SELL';

export interface MarketTick {
  symbol: string;
  price: number;
  timestamp: string;
  volatility: number;
}

export interface Position {
  symbol: string;
  quantity: number;
  averagePrice: number;
  markPrice: number;
  unrealizedPnl: number;
  value: number;
}

export interface ExposureBucket {
  assetClass: string;
  notional: number;
  limit: number;
}

export interface Order {
  id: string;
  symbol: string;
  side: OrderSide;
  quantity: number;
  price: number;
  status: 'ACCEPTED' | 'REJECTED' | 'WORKING' | 'FILLED' | 'CANCELLED';
  createdAt: string;
}

export interface OrderTicketInput {
  symbol: string;
  side: OrderSide;
  quantity: number;
  price: number;
}

export interface RiskMetrics {
  nav: number;
  var95: number;
  expectedShortfall: number;
  maxDrawdown: number;
  leverage: number;
  kellyFraction: number;
  availableBuyingPower: number;
}

export interface PortfolioSnapshot {
  metrics: RiskMetrics;
  positions: Position[];
  exposures: ExposureBucket[];
  equityCurve: number[];
  returns: number[];
  limits: RiskControls;
}

export interface RiskControls {
  maxLeverage: number;
  maxDrawdown: number;
  perTradeVaR: number;
}

export interface OrdersResponse {
  orders: Order[];
}

export interface PortfolioResponse extends PortfolioSnapshot {
  generatedAt: string;
}
