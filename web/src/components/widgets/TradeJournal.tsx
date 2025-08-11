/**
 * Trade Journal widget displaying a list of executed trades.
 */
import React from 'react';

export interface Trade {
  id: string;
  symbol: string;
  qty: number;
  price: number;
}

export const TradeJournal: React.FC<{ trades: Trade[] }> = ({ trades }) => (
  <ul className="p-2 list-disc">
    {trades.map((t) => (
      <li key={t.id}>
        {t.symbol} {t.qty}@{t.price}
      </li>
    ))}
  </ul>
);
