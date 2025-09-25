'use client';

import { useState } from 'react';
import { submitOrder } from '../../lib/api';
import type { PortfolioResponse, OrderTicketInput } from '../../types/trading';

/**
 * Smart order ticket enforcing client-side validation before hitting the API.
 */
interface Props {
  portfolio?: PortfolioResponse;
  onSubmitted: () => void;
}

const defaultForm: OrderTicketInput = {
  symbol: 'BTC-PERP',
  side: 'BUY',
  quantity: 0.25,
  price: 62_050,
};

const OrderForm = ({ portfolio, onSubmitted }: Props): JSX.Element => {
  const [form, setForm] = useState<OrderTicketInput>(defaultForm);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  const validate = (): void => {
    if (!portfolio) {
      throw new Error('Portfolio unavailable');
    }
    if (!form.symbol || form.symbol.length < 3) {
      throw new Error('Symbol must be at least 3 characters');
    }
    if (form.quantity <= 0) {
      throw new Error('Quantity must be positive');
    }
    if (form.price <= 0) {
      throw new Error('Price must be positive');
    }
    const notional = form.quantity * form.price;
    if (notional > portfolio.metrics.availableBuyingPower) {
      throw new Error('Notional exceeds available buying power');
    }
  };

  return (
    <form
      className="mt-4 flex flex-col gap-3"
      onSubmit={async (event) => {
        event.preventDefault();
        setSubmitting(true);
        setError(null);
        setSuccess(null);
        try {
          validate();
          await submitOrder(form);
          setSuccess('Order accepted');
          onSubmitted();
        } catch (err) {
          const message = err instanceof Error ? err.message : 'Unknown error';
          setError(message);
        } finally {
          setSubmitting(false);
        }
      }}
    >
      <label className="flex flex-col text-sm">
        <span className="text-xs uppercase text-zinc-500">Symbol</span>
        <input
          value={form.symbol}
          onChange={(event) => setForm((state) => ({ ...state, symbol: event.target.value.toUpperCase() }))}
          className="mt-1 rounded-md border border-zinc-700 bg-black/40 p-2"
          required
        />
      </label>
      <label className="flex flex-col text-sm">
        <span className="text-xs uppercase text-zinc-500">Side</span>
        <select
          value={form.side}
          onChange={(event) => setForm((state) => ({ ...state, side: event.target.value as OrderTicketInput['side'] }))}
          className="mt-1 rounded-md border border-zinc-700 bg-black/40 p-2"
        >
          <option value="BUY">Buy</option>
          <option value="SELL">Sell</option>
        </select>
      </label>
      <label className="flex flex-col text-sm">
        <span className="text-xs uppercase text-zinc-500">Quantity</span>
        <input
          type="number"
          min={0.0001}
          step={0.0001}
          value={form.quantity}
          onChange={(event) => setForm((state) => ({ ...state, quantity: Number(event.target.value) }))}
          className="mt-1 rounded-md border border-zinc-700 bg-black/40 p-2"
        />
      </label>
      <label className="flex flex-col text-sm">
        <span className="text-xs uppercase text-zinc-500">Limit Price</span>
        <input
          type="number"
          min={1}
          step={0.5}
          value={form.price}
          onChange={(event) => setForm((state) => ({ ...state, price: Number(event.target.value) }))}
          className="mt-1 rounded-md border border-zinc-700 bg-black/40 p-2"
        />
      </label>
      <button
        type="submit"
        disabled={isSubmitting}
        className="rounded-md bg-gradient-to-r from-cyan-500 to-purple-500 p-2 text-sm font-semibold text-black disabled:opacity-50"
      >
        {isSubmitting ? 'Routing…' : 'Route Order'}
      </button>
      {error ? <p className="text-sm text-red-400">{error}</p> : null}
      {success ? <p className="text-sm text-emerald-400">{success}</p> : null}
    </form>
  );
};

export default OrderForm;
