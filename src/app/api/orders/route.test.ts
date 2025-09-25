import { beforeEach, describe, expect, it } from 'vitest';
import { NextRequest } from 'next/server';
import { GET, POST, resetOrderStore } from './route';

/**
 * Tests covering the order API contract.
 */
describe('orders api', () => {
  beforeEach(() => {
    resetOrderStore();
  });

  it('returns seeded orders', async () => {
    const response = await GET();
    const payload = await response.json();
    expect(Array.isArray(payload.orders)).toBe(true);
    expect(payload.orders.length).toBeGreaterThan(0);
  });

  it('rejects risk violating order', async () => {
    const request = new NextRequest('http://localhost/api/orders', {
      method: 'POST',
      body: JSON.stringify({
        symbol: 'BTC-PERP',
        side: 'BUY',
        quantity: 10_000,
        price: 100_000,
      }),
    });
    const response = await POST(request);
    expect(response.status).toBe(400);
  });

  it('accepts order within limits', async () => {
    const request = new NextRequest('http://localhost/api/orders', {
      method: 'POST',
      body: JSON.stringify({
        symbol: 'ETH-PERP',
        side: 'BUY',
        quantity: 1,
        price: 3_200,
      }),
    });
    const response = await POST(request);
    expect(response.status).toBe(201);
  });
});
