import { nanoid } from 'nanoid';
import { z } from 'zod';
import { buildPortfolioSnapshot, calculateDynamicSize } from './risk';
import type { Order, OrderTicketInput, PortfolioSnapshot } from '../types/trading';

/**
 * Order creation utilities enforcing risk constraints before accepting submissions.
 */
export const orderTicketSchema = z.object({
  symbol: z.string().min(3),
  side: z.enum(['BUY', 'SELL']),
  quantity: z.number().positive(),
  price: z.number().positive(),
});

export interface OrderStore {
  portfolio: PortfolioSnapshot;
  orders: Order[];
}

export const createInitialOrderStore = (): OrderStore => ({
  portfolio: buildPortfolioSnapshot(),
  orders: [],
});

export const validateOrderTicket = (ticket: OrderTicketInput, store: OrderStore): void => {
  const parsed = orderTicketSchema.safeParse(ticket);
  if (!parsed.success) {
    throw new Error(parsed.error.flatten().formErrors.join(', '));
  }

  const { portfolio } = store;
  const { metrics, limits } = portfolio;
  const maxPositionSize = calculateDynamicSize(metrics.nav, limits, metrics, ticket.price);
  if (ticket.quantity > maxPositionSize) {
    throw new Error(`Quantity exceeds dynamic risk cap of ${maxPositionSize}`);
  }

  const projectedNotional = ticket.quantity * ticket.price;
  const leverageAfter = (metrics.nav + projectedNotional) / metrics.nav;
  if (leverageAfter > limits.maxLeverage) {
    throw new Error('Order would breach leverage limit');
  }

  if (metrics.maxDrawdown >= limits.maxDrawdown) {
    throw new Error('Trading halted: drawdown limit reached');
  }
};

export const appendOrder = (ticket: OrderTicketInput, store: OrderStore): Order => {
  validateOrderTicket(ticket, store);
  const order: Order = {
    id: nanoid(12),
    symbol: ticket.symbol,
    side: ticket.side,
    quantity: Number(ticket.quantity.toFixed(4)),
    price: Number(ticket.price.toFixed(2)),
    status: 'ACCEPTED',
    createdAt: new Date().toISOString(),
  };
  store.orders = [order, ...store.orders];
  return order;
};
