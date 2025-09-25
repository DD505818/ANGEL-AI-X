import type { ExposureBucket, Order, Position, PortfolioSnapshot } from '../types/trading';

/**
 * Deterministic sample data powering the demo environment.
 */
export const samplePositions: Position[] = [
  {
    symbol: 'BTC-PERP',
    quantity: 1.5,
    averagePrice: 61_240,
    markPrice: 62_120,
    unrealizedPnl: 1_320,
    value: 93_180,
  },
  {
    symbol: 'ETH-PERP',
    quantity: 10,
    averagePrice: 3_120,
    markPrice: 3_180,
    unrealizedPnl: 600,
    value: 31_800,
  },
  {
    symbol: 'SOL-PERP',
    quantity: 400,
    averagePrice: 148.4,
    markPrice: 152.1,
    unrealizedPnl: 1_480,
    value: 60_840,
  },
];

export const sampleExposures: ExposureBucket[] = [
  { assetClass: 'Layer1', notional: 110_000, limit: 150_000 },
  { assetClass: 'DeFi', notional: 42_000, limit: 80_000 },
  { assetClass: 'AI', notional: 28_000, limit: 60_000 },
  { assetClass: 'PerpBasis', notional: 65_000, limit: 100_000 },
];

export const sampleReturns: number[] = [
  0.012,
  -0.006,
  0.008,
  0.004,
  -0.01,
  0.005,
  0.011,
  -0.002,
  0.009,
  0.007,
  -0.004,
  0.006,
  0.005,
  -0.003,
  0.008,
  0.01,
  -0.007,
  0.004,
  0.006,
  -0.002,
];

export const sampleEquityCurve: number[] = sampleReturns.reduce<number[]>((curve, r) => {
  const last = curve[curve.length - 1];
  const next = last * (1 + r);
  return [...curve, Math.round(next)];
}, [1_000_000]);

export const initialOrders: Order[] = [
  {
    id: 'ord-1',
    symbol: 'BTC-PERP',
    side: 'BUY',
    quantity: 0.75,
    price: 62_000,
    status: 'WORKING',
    createdAt: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
  },
  {
    id: 'ord-2',
    symbol: 'ETH-PERP',
    side: 'SELL',
    quantity: 5,
    price: 3_220,
    status: 'FILLED',
    createdAt: new Date(Date.now() - 1000 * 60 * 40).toISOString(),
  },
];

export const sampleSnapshot: PortfolioSnapshot = {
  metrics: {
    nav: 1_250_000,
    var95: 18_200,
    expectedShortfall: 24_900,
    maxDrawdown: 0.14,
    leverage: 2.4,
    kellyFraction: 0.23,
    availableBuyingPower: 520_000,
  },
  positions: samplePositions,
  exposures: sampleExposures,
  equityCurve: sampleEquityCurve,
  returns: sampleReturns,
  limits: {
    maxLeverage: 3,
    maxDrawdown: 0.2,
    perTradeVaR: 12_000,
  },
};
