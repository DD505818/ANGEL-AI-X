import { describe, expect, it } from 'vitest';
import { useRiskStore } from '../src/store/useRiskStore';

describe('useRiskStore', () => {
  it('toggles kill switch', () => {
    const { killSwitch, toggleKillSwitch } = useRiskStore.getState();
    expect(killSwitch).toBe(false);
    toggleKillSwitch();
    expect(useRiskStore.getState().killSwitch).toBe(true);
  });
});
