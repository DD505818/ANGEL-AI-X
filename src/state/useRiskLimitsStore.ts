'use client';

import type { StateCreator } from 'zustand';
import { create } from 'zustand';
import type { RiskControls } from '../types/trading';

/**
 * Zustand store tracking operator-configurable risk guardrails.
 */
interface RiskLimitsState {
  limits: RiskControls;
  setLimits: (limits: Partial<RiskControls>) => void;
}

const createState: StateCreator<RiskLimitsState> = (set) => ({
  limits: {
    maxLeverage: 3,
    maxDrawdown: 0.2,
    perTradeVaR: 12_000,
  },
  setLimits: (limits) =>
    set((state) => ({
      limits: { ...state.limits, ...limits },
    })),
});

export const useRiskLimitsStore = create<RiskLimitsState>(createState);

export const resetRiskLimitsStore = (): void => {
  useRiskLimitsStore.setState({
    limits: {
      maxLeverage: 3,
      maxDrawdown: 0.2,
      perTradeVaR: 12_000,
    },
  });
};
