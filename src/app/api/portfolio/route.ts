import { NextResponse } from 'next/server';
import { buildPortfolioSnapshot } from '../../../lib/risk';
import type { PortfolioResponse } from '../../../types/trading';

/**
 * Portfolio API exposing deterministic portfolio and risk metrics.
 */
export async function GET(): Promise<NextResponse<PortfolioResponse>> {
  const snapshot = buildPortfolioSnapshot();
  return NextResponse.json({ ...snapshot, generatedAt: new Date().toISOString() });
}
