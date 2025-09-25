import { describe, expect, it } from 'vitest';
import { appendOrder, createInitialOrderStore } from './orders';

/**
 * Order helper tests ensuring risk validation is enforced.
 */
describe('orders', () => {
  it('rejects orders breaching leverage', () => {
    const store = createInitialOrderStore();
    expect(() =>
      appendOrder(
        {
          symbol: 'BTC-PERP',
          side: 'BUY',
          quantity: 10_000,
          price: 100_000,
        },
        store,
      ),
    ).toThrow(/risk cap/i);
  });

  it('accepts valid order', () => {
    const store = createInitialOrderStore();
    const order = appendOrder(
      {
        symbol: 'BTC-PERP',
        side: 'BUY',
        quantity: 0.1,
        price: 62_000,
      },
      store,
    );
    expect(order.status).toBe('ACCEPTED');
    expect(store.orders).toContain(order);
  });
});
