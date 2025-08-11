/**
 * useRiskStore manages global risk controls.
 */
import { create } from 'zustand';

export interface RiskState {
  killSwitch: boolean;
  maxDrawdown: number;
  toggleKillSwitch: () => void;
  setMaxDrawdown: (value: number) => void;
}

export const useRiskStore = create<RiskState>((set) => ({
  killSwitch: false,
  maxDrawdown: 0.2,
  toggleKillSwitch: () => set((s) => ({ killSwitch: !s.killSwitch })),
  setMaxDrawdown: (value: number) => set({ maxDrawdown: value }),
}));
