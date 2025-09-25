'use client';

import type { FC } from 'react';
import type { PortfolioResponse } from '../../types/trading';

/**
 * Positions grid summarizing mark-to-market details.
 */
interface Props {
  portfolio?: PortfolioResponse;
}

const PositionsTable: FC<Props> = ({ portfolio }) => {
  if (!portfolio) {
    return <p className="mt-4 text-sm text-zinc-400">Loading positions…</p>;
  }

  return (
    <div className="mt-4 overflow-x-auto">
      <table className="min-w-full divide-y divide-zinc-800 text-sm">
        <thead className="bg-black/40">
          <tr>
            <th className="px-3 py-2 text-left font-medium">Symbol</th>
            <th className="px-3 py-2 text-right font-medium">Quantity</th>
            <th className="px-3 py-2 text-right font-medium">Average</th>
            <th className="px-3 py-2 text-right font-medium">Mark</th>
            <th className="px-3 py-2 text-right font-medium">P&L</th>
            <th className="px-3 py-2 text-right font-medium">Value</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-900">
          {portfolio.positions.map((position) => (
            <tr key={position.symbol} className="bg-black/20">
              <td className="px-3 py-2 font-mono">{position.symbol}</td>
              <td className="px-3 py-2 text-right">{position.quantity.toLocaleString()}</td>
              <td className="px-3 py-2 text-right">${position.averagePrice.toLocaleString()}</td>
              <td className="px-3 py-2 text-right">${position.markPrice.toLocaleString()}</td>
              <td
                className={`px-3 py-2 text-right ${position.unrealizedPnl >= 0 ? 'text-emerald-400' : 'text-red-400'}`}
              >
                ${position.unrealizedPnl.toLocaleString()}
              </td>
              <td className="px-3 py-2 text-right">${position.value.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PositionsTable;
