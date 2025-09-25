'use client';

import { useEffect, useRef, useState } from 'react';
import type { MarketTick } from '../types/trading';

/**
 * Subscribes to the market SSE feed with exponential back-off reconnection.
 */
export const useMarketFeed = (url: string) => {
  const [ticks, setTicks] = useState<MarketTick[]>([]);
  const [status, setStatus] = useState<'connecting' | 'open' | 'retrying'>('connecting');
  const retryRef = useRef(1000);
  const closedRef = useRef(false);

  useEffect(() => {
    closedRef.current = false;
    let eventSource: EventSource | null = null;
    let retryHandle: ReturnType<typeof setTimeout> | null = null;

    const connect = () => {
      setStatus('connecting');
      eventSource = new EventSource(url);
      eventSource.onopen = () => {
        retryRef.current = 1000;
        setStatus('open');
      };
      eventSource.onmessage = (event) => {
        if (!event.data) {
          return;
        }
        try {
          const payload = JSON.parse(event.data) as MarketTick;
          setTicks((current) => [payload, ...current].slice(0, 100));
        } catch (error) {
          console.error('Failed to parse market event', error);
        }
      };
      eventSource.onerror = () => {
        if (closedRef.current) {
          return;
        }
        setStatus('retrying');
        eventSource?.close();
        const retryMs = Math.min(retryRef.current, 15_000);
        retryHandle = setTimeout(connect, retryMs);
        retryRef.current = Math.min(retryRef.current * 2, 30_000);
      };
    };

    connect();

    return () => {
      closedRef.current = true;
      eventSource?.close();
      if (retryHandle) {
        clearTimeout(retryHandle);
      }
    };
  }, [url]);

  return { ticks, status } as const;
};
