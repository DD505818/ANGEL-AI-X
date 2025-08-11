/**
 * PnL Sparkline widget rendering a miniature performance chart.
 */
import React from 'react';

export const PnLSparkline: React.FC<{ data: number[] }> = ({ data }) => {
  const points = data
    .map((d, i) => `${(i / Math.max(data.length - 1, 1)) * 100},${100 - d}`)
    .join(' ');
  return (
    <svg viewBox="0 0 100 100" className="w-full h-20">
      <polyline fill="none" stroke="currentColor" strokeWidth="2" points={points} />
    </svg>
  );
};
