import { describe, expect, it } from 'vitest';
import { GET } from './route';

/**
 * Tests covering the portfolio API contract.
 */
describe('portfolio api', () => {
  it('returns portfolio snapshot', async () => {
    const response = await GET();
    const payload = await response.json();
    expect(payload.metrics.nav).toBeGreaterThan(0);
    expect(Array.isArray(payload.positions)).toBe(true);
    expect(payload.generatedAt).toBeDefined();
  });
});
