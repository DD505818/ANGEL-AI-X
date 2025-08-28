'use client';
import { useState } from 'react';

export default function BacktestPage() {
  const [summary, setSummary] = useState(null);

  async function run() {
    const res = await fetch('/api/quantum/backtest', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const data = await res.json();
    setSummary(data.summary);
  }

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Backtest Runner</h1>
      <button onClick={run} className="mt-2 rounded bg-blue-500 px-4 py-2 text-white">Run</button>
      {summary && <pre className="mt-4 text-sm">{JSON.stringify(summary, null, 2)}</pre>}
    </div>
  );
}
