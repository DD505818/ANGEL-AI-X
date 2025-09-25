import { sampleSnapshot } from './data';
import type { PortfolioSnapshot, RiskControls, RiskMetrics } from '../types/trading';

/**
 * Risk utility helpers implementing VaR, expected shortfall, drawdown, and Kelly sizing.
 */
export const calculateHistoricalVar = (returns: number[], confidence: number): number => {
  if (returns.length === 0) {
    throw new Error('returns must be non-empty');
  }
  if (confidence <= 0 || confidence >= 1) {
    throw new Error('confidence must be between 0 and 1');
  }
  const sorted = [...returns].sort((a, b) => a - b);
  const index = Math.floor((1 - confidence) * sorted.length);
  const varLoss = sorted[index] ?? sorted[0];
  return Math.abs(varLoss);
};

export const calculateExpectedShortfall = (returns: number[], confidence: number): number => {
  if (returns.length === 0) {
    throw new Error('returns must be non-empty');
  }
  if (confidence <= 0 || confidence >= 1) {
    throw new Error('confidence must be between 0 and 1');
  }
  const sorted = [...returns].sort((a, b) => a - b);
  const cutoffIndex = Math.floor((1 - confidence) * sorted.length);
  const tail = sorted.slice(0, Math.max(1, cutoffIndex));
  const avg = tail.reduce((sum, value) => sum + value, 0) / tail.length;
  return Math.abs(avg);
};

export const calculateMaxDrawdown = (equityCurve: number[]): number => {
  if (equityCurve.length < 2) {
    return 0;
  }
  let peak = equityCurve[0];
  let maxDrawdown = 0;
  for (const point of equityCurve) {
    if (point > peak) {
      peak = point;
    }
    const drawdown = (peak - point) / peak;
    if (drawdown > maxDrawdown) {
      maxDrawdown = drawdown;
    }
  }
  return Number(maxDrawdown.toFixed(4));
};

export const calculateKellyFraction = (winRate: number, winLossRatio: number): number => {
  if (winRate < 0 || winRate > 1) {
    throw new Error('winRate must be between 0 and 1');
  }
  if (winLossRatio <= 0) {
    throw new Error('winLossRatio must be positive');
  }
  const fraction = winRate - (1 - winRate) / winLossRatio;
  return Math.max(0, Number(fraction.toFixed(4)));
};

export const calculateDynamicSize = (
  equity: number,
  riskControls: RiskControls,
  metrics: RiskMetrics,
  price: number,
): number => {
  const riskBudget = Math.min(riskControls.perTradeVaR, metrics.availableBuyingPower * 0.1);
  const allowableDrawdown = Math.max(0, riskControls.maxDrawdown - metrics.maxDrawdown);
  const kellyMultiplier = metrics.kellyFraction * allowableDrawdown;
  const baseSize = riskBudget / Math.max(price, 1);
  const size = baseSize * (1 + kellyMultiplier);
  return Number(size.toFixed(4));
};

export const buildPortfolioSnapshot = (): PortfolioSnapshot => {
  const { equityCurve, returns, metrics, exposures, positions, limits } = sampleSnapshot;
  const var95 = calculateHistoricalVar(returns, 0.95) * metrics.nav;
  const expectedShortfall = calculateExpectedShortfall(returns, 0.95) * metrics.nav;
  const maxDrawdown = calculateMaxDrawdown(equityCurve);
  const kellyFraction = calculateKellyFraction(0.58, 1.9);

  const derivedMetrics: RiskMetrics = {
    ...metrics,
    var95: Number(var95.toFixed(2)),
    expectedShortfall: Number(expectedShortfall.toFixed(2)),
    maxDrawdown,
    kellyFraction,
  };

  return {
    metrics: derivedMetrics,
    positions,
    exposures,
    equityCurve,
    returns,
    limits,
  };
};
