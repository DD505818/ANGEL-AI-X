/**
 * Utility functions for dynamic position sizing.
 */
export function kelly(p: number, b: number): number {
  if (b <= 0) throw new Error('b must be > 0');
  if (p <= 0 || p >= 1) throw new Error('p must be between 0 and 1');
  return Math.max(0, (p * (b + 1) - 1) / b);
}

export function valueAtRisk(returns: number[], confidence: number): number {
  if (confidence <= 0 || confidence >= 1) throw new Error('confidence must be between 0 and 1');
  const sorted = [...returns].sort((a, b) => a - b);
  const index = Math.floor((1 - confidence) * sorted.length);
  return Math.abs(sorted[index] ?? 0);
}
