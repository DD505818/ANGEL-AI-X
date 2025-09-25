import type { NextRequest } from 'next/server';

/**
 * Streaming market data feed producing synthetic ticks via server-sent events.
 */
export async function GET(_request: NextRequest): Promise<Response> {
  const encoder = new TextEncoder();
  let price = 62_000;
  let volatility = 0.02;

  let stop: (() => void) | null = null;

  const stream = new ReadableStream<Uint8Array>({
    start(controller) {
      controller.enqueue(encoder.encode('retry: 1000\n\n'));
      const interval = setInterval(() => {
        const drift = Math.sin(Date.now() / 60000) * 0.5;
        const shock = (Math.random() - 0.5) * volatility * price;
        price = Math.max(1, price + drift + shock);
        volatility = Math.min(0.08, Math.max(0.01, volatility + (Math.random() - 0.5) * 0.002));

        const payload = {
          symbol: 'BTC-PERP',
          price: Number(price.toFixed(2)),
          timestamp: new Date().toISOString(),
          volatility: Number(volatility.toFixed(4)),
        };
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(payload)}\n\n`));
      }, 1000);

      const heartbeat = setInterval(() => {
        controller.enqueue(encoder.encode(': keep-alive\n\n'));
      }, 15_000);

      controller.enqueue(encoder.encode('event: ready\ndata: {}\n\n'));

      stop = () => {
        clearInterval(interval);
        clearInterval(heartbeat);
        try {
          controller.close();
        } catch (error) {
          console.error('Failed to close market feed stream', error);
        }
      };
    },
    cancel() {
      stop?.();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      Connection: 'keep-alive',
    },
  });
}
