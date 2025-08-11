/**
 * Signal Log widget listing recent trading signals.
 */
import React from 'react';

export interface Signal {
  id: string;
  message: string;
}

export const SignalLog: React.FC<{ signals: Signal[] }> = ({ signals }) => (
  <ul className="p-2 list-disc">
    {signals.map((s) => (
      <li key={s.id}>{s.message}</li>
    ))}
  </ul>
);
