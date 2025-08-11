/**
 * useMarketData streams price updates over WebSocket with auto-reconnect.
 */
import { useEffect, useState } from 'react';

const WS_URL = process.env.WS_URL ?? '';

export default function useMarketData(): number {
  const [price, setPrice] = useState(0);

  useEffect((): (() => void) => {
    let ws: WebSocket | null = null;
    let timer: NodeJS.Timeout;

    const connect = (): void => {
      ws = new WebSocket(WS_URL);
      ws.onmessage = (event): void => {
        try {
          const data = JSON.parse(event.data);
          if (typeof data.price === 'number') setPrice(data.price);
        } catch {
          /* ignore malformed messages */
        }
      };
      ws.onclose = (): void => {
        timer = setTimeout(connect, 1000);
      };
    };

    connect();
    return (): void => {
      if (ws) ws.close();
      clearTimeout(timer);
    };
  }, []);

  return price;
}
