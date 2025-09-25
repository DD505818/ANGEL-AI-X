'use client';

import type { FC } from 'react';
import type { Order } from '../../types/trading';

/**
 * Tabular presentation of recently routed orders.
 */
interface Props {
  orders: Order[];
  isLoading: boolean;
}

const OrdersTable: FC<Props> = ({ orders, isLoading }) => {
  if (isLoading) {
    return <div className="mt-4 h-32 animate-pulse rounded-md bg-black/40" />;
  }

  if (orders.length === 0) {
    return <p className="mt-4 text-sm text-zinc-400">No orders submitted.</p>;
  }

  return (
    <div className="mt-4 overflow-x-auto">
      <table className="min-w-full divide-y divide-zinc-800 text-sm">
        <thead className="bg-black/40">
          <tr>
            <th className="px-3 py-2 text-left font-medium">Symbol</th>
            <th className="px-3 py-2 text-left font-medium">Side</th>
            <th className="px-3 py-2 text-right font-medium">Quantity</th>
            <th className="px-3 py-2 text-right font-medium">Price</th>
            <th className="px-3 py-2 text-left font-medium">Status</th>
            <th className="px-3 py-2 text-left font-medium">Created</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-900">
          {orders.map((order) => (
            <tr key={order.id} className="bg-black/20">
              <td className="px-3 py-2 font-mono">{order.symbol}</td>
              <td className={`px-3 py-2 font-semibold ${order.side === 'BUY' ? 'text-emerald-400' : 'text-red-400'}`}>
                {order.side}
              </td>
              <td className="px-3 py-2 text-right">{order.quantity.toLocaleString()}</td>
              <td className="px-3 py-2 text-right">${order.price.toLocaleString()}</td>
              <td className="px-3 py-2">{order.status}</td>
              <td className="px-3 py-2 text-zinc-400">{new Date(order.createdAt).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default OrdersTable;
