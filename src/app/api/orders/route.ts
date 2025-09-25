import { NextRequest, NextResponse } from 'next/server';
import { initialOrders } from '../../../lib/data';
import { appendOrder, createInitialOrderStore } from '../../../lib/orders';
import type { OrderStore } from '../../../lib/orders';
import type { OrdersResponse, OrderTicketInput } from '../../../types/trading';

/**
 * Order management API enforcing deterministic risk checks before acceptance.
 */
const globalState = globalThis as typeof globalThis & { __angelOrderStore?: OrderStore };

if (!globalState.__angelOrderStore) {
  const store = createInitialOrderStore();
  store.orders = [...initialOrders];
  globalState.__angelOrderStore = store;
}

export const getOrderStore = (): OrderStore => {
  return globalState.__angelOrderStore as OrderStore;
};

export async function GET(): Promise<NextResponse<OrdersResponse>> {
  const store = getOrderStore();
  return NextResponse.json({ orders: store.orders });
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = (await request.json()) as OrderTicketInput;
    const store = getOrderStore();
    const order = appendOrder(body, store);
    return NextResponse.json(order, { status: 201 });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 400 });
  }
}

export const resetOrderStore = (): void => {
  const store = createInitialOrderStore();
  store.orders = [...initialOrders];
  globalState.__angelOrderStore = store;
};
