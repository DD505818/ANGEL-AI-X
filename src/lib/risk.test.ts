import { describe, expect, it } from 'vitest';
import {
  calculateDynamicSize,
  calculateExpectedShortfall,
  calculateHistoricalVar,
  calculateKellyFraction,
  calculateMaxDrawdown,
} from './risk';
import { sampleSnapshot } from './data';

/**
 * Unit tests validating risk math helpers.
 */
describe('risk helpers', () => {
  it('computes historical VaR', () => {
    const result = calculateHistoricalVar([0.01, -0.02, 0.03, -0.01], 0.95);
    expect(result).toBeGreaterThan(0);
  });

  it('computes expected shortfall', () => {
    const result = calculateExpectedShortfall([0.01, -0.02, 0.03, -0.01], 0.95);
    expect(result).toBeGreaterThan(0);
  });

  it('computes max drawdown', () => {
    const result = calculateMaxDrawdown([100, 95, 120, 80, 140]);
    expect(result).toBeCloseTo(0.3333, 3);
  });

  it('computes Kelly fraction', () => {
    const result = calculateKellyFraction(0.55, 1.8);
    expect(result).toBeGreaterThan(0);
  });

  it('computes dynamic size respecting risk limits', () => {
    const metrics = sampleSnapshot.metrics;
    const limits = sampleSnapshot.limits;
    const size = calculateDynamicSize(metrics.nav, limits, metrics, 62_000);
    expect(size).toBeGreaterThan(0);
  });
});
