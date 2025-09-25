import { render, screen } from '@testing-library/react';
import { afterEach, test, vi } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Home from './page';

afterEach(() => {
  vi.unstubAllGlobals();
});

test('renders dashboard heading', async () => {
  const queryClient = new QueryClient();
  vi.stubGlobal(
    'fetch',
    vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            metrics: {
              nav: 1_000_000,
              var95: 10_000,
              expectedShortfall: 15_000,
              maxDrawdown: 0.1,
              leverage: 2,
              kellyFraction: 0.2,
              availableBuyingPower: 500_000,
            },
            positions: [],
            exposures: [],
            equityCurve: [],
            returns: [],
            limits: { maxLeverage: 3, maxDrawdown: 0.2, perTradeVaR: 12_000 },
            generatedAt: new Date().toISOString(),
          }),
      })
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ orders: [] }) }),
  );

  class MockEventSource {
    onopen: ((event: Event) => void) | null = null;
    onmessage: ((event: MessageEvent) => void) | null = null;
    onerror: ((event: Event) => void) | null = null;
    constructor(public readonly url: string) {
      setTimeout(() => {
        this.onopen?.(new Event('open'));
      }, 0);
    }
    close(): void {
      // noop
    }
  }

  vi.stubGlobal('EventSource', MockEventSource);

  render(
    <QueryClientProvider client={queryClient}>
      <Home />
    </QueryClientProvider>,
  );
  expect(await screen.findByText('ANGEL.AI Execution Mesh')).toBeInTheDocument();
});
