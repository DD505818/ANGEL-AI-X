'use client';

import { useEffect, useMemo, useState } from 'react';
import { useRiskLimitsStore } from '../../state/useRiskLimitsStore';
import type { PortfolioResponse } from '../../types/trading';

/**
 * Displays current risk metrics and allows operators to tune guardrails.
 */
interface Props {
  portfolio?: PortfolioResponse;
}

const RiskLimitsCard = ({ portfolio }: Props): JSX.Element => {
  const { limits, setLimits } = useRiskLimitsStore();
  const [formState, setFormState] = useState(limits);

  useEffect(() => {
    setFormState(limits);
  }, [limits]);

  const breaches = useMemo(() => {
    if (!portfolio) {
      return [] as string[];
    }
    const items: string[] = [];
    if (portfolio.metrics.maxDrawdown > limits.maxDrawdown) {
      items.push('Drawdown breach');
    }
    if (portfolio.metrics.leverage > limits.maxLeverage) {
      items.push('Leverage breach');
    }
    if (portfolio.metrics.var95 > limits.perTradeVaR) {
      items.push('VaR budget exceeded');
    }
    return items;
  }, [portfolio, limits]);

  return (
    <div className="flex flex-col gap-4">
      <div>
        <p className="text-sm text-zinc-400">Limits</p>
        <form
          className="mt-2 grid grid-cols-1 gap-3"
          onSubmit={(event) => {
            event.preventDefault();
            setLimits(formState);
          }}
        >
          <label className="flex flex-col text-sm">
            <span className="text-xs uppercase text-zinc-500">Max Leverage</span>
            <input
              type="number"
              min={1}
              step={0.1}
              value={formState.maxLeverage}
              onChange={(event) =>
                setFormState((state) => ({ ...state, maxLeverage: Number(event.target.value) }))
              }
              className="mt-1 rounded-md border border-zinc-700 bg-black/40 p-2"
            />
          </label>
          <label className="flex flex-col text-sm">
            <span className="text-xs uppercase text-zinc-500">Max Drawdown</span>
            <input
              type="number"
              min={0.05}
              max={0.5}
              step={0.01}
              value={formState.maxDrawdown}
              onChange={(event) =>
                setFormState((state) => ({ ...state, maxDrawdown: Number(event.target.value) }))
              }
              className="mt-1 rounded-md border border-zinc-700 bg-black/40 p-2"
            />
          </label>
          <label className="flex flex-col text-sm">
            <span className="text-xs uppercase text-zinc-500">Per Trade VaR</span>
            <input
              type="number"
              min={1000}
              step={500}
              value={formState.perTradeVaR}
              onChange={(event) =>
                setFormState((state) => ({ ...state, perTradeVaR: Number(event.target.value) }))
              }
              className="mt-1 rounded-md border border-zinc-700 bg-black/40 p-2"
            />
          </label>
          <button
            type="submit"
            className="rounded-md bg-gradient-to-r from-cyan-500 to-purple-500 p-2 text-sm font-semibold text-black"
          >
            Update Limits
          </button>
        </form>
      </div>
      <div>
        <p className="text-sm text-zinc-400">Breaches</p>
        {breaches.length === 0 ? (
          <p className="mt-2 text-sm text-emerald-400">All clear</p>
        ) : (
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-red-400">
            {breaches.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default RiskLimitsCard;
