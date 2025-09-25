import { describe, expect, it, vi, afterEach } from 'vitest';
import { fetchOrders, fetchPortfolio, submitOrder } from './api';

/**
 * Tests ensuring API client helpers interpret responses correctly.
 */
describe('api helpers', () => {
  afterEach(() => {
    vi.resetAllMocks();
    vi.unstubAllGlobals();
  });

  it('fetches portfolio', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: () =>
          Promise.resolve({
            metrics: {
              nav: 1,
              var95: 0,
              expectedShortfall: 0,
              maxDrawdown: 0,
              leverage: 1,
              kellyFraction: 0,
              availableBuyingPower: 0,
            },
            positions: [],
            exposures: [],
            equityCurve: [],
            returns: [],
            limits: { maxLeverage: 1, maxDrawdown: 0.1, perTradeVaR: 1 },
            generatedAt: new Date().toISOString(),
          }),
      }),
    );
    const response = await fetchPortfolio();
    expect(response.metrics.nav).toBe(1);
  });

  it('throws on error response', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, text: () => 'bad', statusText: 'bad' }));
    await expect(submitOrder({ symbol: 'BTC', side: 'BUY', quantity: 1, price: 1 })).rejects.toThrow();
  });

  it('fetches orders', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: true, json: () => Promise.resolve({ orders: [] }) }),
    );
    const response = await fetchOrders();
    expect(Array.isArray(response.orders)).toBe(true);
  });
});
