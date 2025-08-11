/**
 * Portfolio Globe widget summarizing positions by total value.
 */
import React from 'react';

export interface Position {
  lat: number;
  lng: number;
  value: number;
}

export const PortfolioGlobe: React.FC<{ positions: Position[] }> = ({ positions }) => {
  const total = positions.reduce((acc, p) => acc + p.value, 0);
  return (
    <div className="p-2">
      <h3 className="font-bold">Portfolio Value</h3>
      <p>{total.toFixed(2)}</p>
    </div>
  );
};
