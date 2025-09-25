'use client';

import { useMarketFeed } from '../../hooks/useMarketFeed';

/**
 * Visualizes the live market data feed.
 */
const MarketFeedPanel = (): JSX.Element => {
  const { ticks, status } = useMarketFeed('/api/market');
  const latest = ticks[0];

  return (
    <div className="mt-4 flex flex-col gap-3">
      <div>
        <p className="text-xs uppercase text-zinc-500">Connection</p>
        <p className="text-sm font-semibold text-zinc-300">{status}</p>
      </div>
      {latest ? (
        <div className="rounded-md border border-zinc-700 bg-black/40 p-4">
          <p className="text-xs uppercase text-zinc-500">{latest.symbol}</p>
          <p className="text-2xl font-bold text-emerald-400">${latest.price.toLocaleString()}</p>
          <p className="text-xs text-zinc-400">
            Volatility {(latest.volatility * 100).toFixed(2)}% ·{' '}
            {new Date(latest.timestamp).toLocaleTimeString()}
          </p>
        </div>
      ) : (
        <p className="text-sm text-zinc-400">Waiting for first tick…</p>
      )}
      <div className="max-h-48 overflow-y-auto text-xs text-zinc-400">
        <ul className="space-y-1">
          {ticks.map((tick) => (
            <li key={tick.timestamp} className="flex justify-between font-mono">
              <span>{new Date(tick.timestamp).toLocaleTimeString()}</span>
              <span>${tick.price.toLocaleString()}</span>
              <span>{(tick.volatility * 100).toFixed(2)}%</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default MarketFeedPanel;
