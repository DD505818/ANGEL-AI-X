'use client';

import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, ReferenceLine } from 'recharts';
import type { FC } from 'react';
import type { PortfolioResponse } from '../../types/trading';

/**
 * Visualizes sector exposures relative to configured limits.
 */
interface Props {
  portfolio?: PortfolioResponse;
}

const ExposureHeatmap: FC<Props> = ({ portfolio }) => {
  if (!portfolio) {
    return <p className="mt-4 text-sm text-zinc-400">Loading exposures…</p>;
  }

  const data = portfolio.exposures.map((exposure) => ({
    name: exposure.assetClass,
    notional: exposure.notional,
    limit: exposure.limit,
    utilization: Number(((exposure.notional / exposure.limit) * 100).toFixed(2)),
  }));

  return (
    <div className="mt-4 h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="name" stroke="#a1a1aa" />
          <YAxis stroke="#a1a1aa" tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`} />
          <Tooltip
            contentStyle={{ backgroundColor: 'rgba(17,24,39,0.95)', border: '1px solid #27272a' }}
            formatter={(value: number, _name, entry) => {
              if (entry.dataKey === 'utilization') {
                return [`${value.toFixed(2)}%`, 'Utilization'];
              }
              return [`$${value.toLocaleString()}`, entry.dataKey === 'notional' ? 'Notional' : 'Limit'];
            }}
          />
          <ReferenceLine y={0} stroke="#27272a" />
          <Bar dataKey="limit" fill="#1d4ed8" opacity={0.3} />
          <Bar dataKey="notional" fill="#22d3ee" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ExposureHeatmap;
