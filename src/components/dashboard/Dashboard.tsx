'use client';

import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchOrders, fetchPortfolio } from '../../lib/api';
import MarketFeedPanel from './MarketFeedPanel';
import OrdersTable from './OrdersTable';
import OrderForm from './OrderForm';
import RiskLimitsCard from './RiskLimitsCard';
import ExposureHeatmap from './ExposureHeatmap';
import PositionsTable from './PositionsTable';

/**
 * High-level dashboard orchestrating data queries and layout.
 */
const Dashboard = (): JSX.Element => {
  const portfolioQuery = useQuery({
    queryKey: ['portfolio'],
    queryFn: fetchPortfolio,
    refetchInterval: 60_000,
  });

  const ordersQuery = useQuery({
    queryKey: ['orders'],
    queryFn: fetchOrders,
    refetchInterval: 15_000,
  });

  const stats = useMemo(() => {
    if (!portfolioQuery.data) {
      return [];
    }
    const { metrics } = portfolioQuery.data;
    return [
      { label: 'Net Asset Value', value: `$${metrics.nav.toLocaleString()}` },
      { label: 'VaR 95%', value: `$${metrics.var95.toLocaleString()}` },
      { label: 'Expected Shortfall', value: `$${metrics.expectedShortfall.toLocaleString()}` },
      { label: 'Max Drawdown', value: `${(metrics.maxDrawdown * 100).toFixed(2)}%` },
      { label: 'Kelly Fraction', value: `${(metrics.kellyFraction * 100).toFixed(2)}%` },
      { label: 'Buying Power', value: `$${metrics.availableBuyingPower.toLocaleString()}` },
    ];
  }, [portfolioQuery.data]);

  return (
    <div className="flex min-h-screen flex-col gap-6 p-6">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold">ANGEL.AI Execution Mesh</h1>
        <p className="text-sm text-zinc-400">
          Governance-aligned execution with deterministic risk controls.
        </p>
      </header>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {portfolioQuery.isLoading
          ? Array.from({ length: 3 }).map((_, index) => (
              <div key={index} className="glass-card h-24 animate-pulse" />
            ))
          : stats.map((stat) => (
              <div key={stat.label} className="glass-card p-4">
                <p className="text-xs uppercase tracking-wide text-zinc-400">{stat.label}</p>
                <p className="mt-2 text-2xl font-bold">{stat.value}</p>
              </div>
            ))}
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="glass-card col-span-2 p-4">
          <h2 className="text-lg font-semibold">Positions</h2>
          <PositionsTable portfolio={portfolioQuery.data} />
        </div>
        <div className="glass-card p-4">
          <h2 className="text-lg font-semibold">Risk Controls</h2>
          <RiskLimitsCard portfolio={portfolioQuery.data} />
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="glass-card col-span-2 p-4">
          <h2 className="text-lg font-semibold">Exposures</h2>
          <ExposureHeatmap portfolio={portfolioQuery.data} />
        </div>
        <div className="glass-card p-4">
          <h2 className="text-lg font-semibold">Live Market Feed</h2>
          <MarketFeedPanel />
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="glass-card col-span-2 p-4">
          <h2 className="text-lg font-semibold">Order Blotter</h2>
          <OrdersTable orders={ordersQuery.data?.orders ?? []} isLoading={ordersQuery.isLoading} />
        </div>
        <div className="glass-card p-4">
          <h2 className="text-lg font-semibold">Smart Order Ticket</h2>
          <OrderForm
            portfolio={portfolioQuery.data}
            onSubmitted={() => {
              void ordersQuery.refetch();
              void portfolioQuery.refetch();
            }}
          />
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
