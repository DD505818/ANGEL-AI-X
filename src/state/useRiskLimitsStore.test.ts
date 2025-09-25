import { afterEach, describe, expect, it } from 'vitest';
import { resetRiskLimitsStore, useRiskLimitsStore } from './useRiskLimitsStore';

/**
 * Tests for the risk limits Zustand store.
 */
describe('useRiskLimitsStore', () => {
  afterEach(() => {
    resetRiskLimitsStore();
  });

  it('updates limits', () => {
    const { limits, setLimits } = useRiskLimitsStore.getState();
    expect(limits.maxLeverage).toBe(3);
    setLimits({ maxLeverage: 2.5 });
    expect(useRiskLimitsStore.getState().limits.maxLeverage).toBe(2.5);
  });
});
