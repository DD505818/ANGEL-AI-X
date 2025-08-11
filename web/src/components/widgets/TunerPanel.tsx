/**
 * Tuner Panel widget allowing runtime risk adjustment.
 */
import React, { useState } from 'react';

export const TunerPanel: React.FC = () => {
  const [risk, setRisk] = useState(0.5);
  return (
    <div className="p-2">
      <h3 className="font-bold">Risk</h3>
      <input
        type="range"
        min={0}
        max={1}
        step={0.1}
        value={risk}
        onChange={(e) => setRisk(Number(e.target.value))}
      />
      <span>{risk.toFixed(1)}</span>
    </div>
  );
};
