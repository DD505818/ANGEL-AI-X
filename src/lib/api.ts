import type { OrdersResponse, PortfolioResponse, OrderTicketInput, Order } from '../types/trading';

/**
 * Typed HTTP helpers for querying the Next.js API routes.
 */
const handleResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || response.statusText);
  }
  return (await response.json()) as T;
};

export const fetchPortfolio = async (): Promise<PortfolioResponse> => {
  const response = await fetch('/api/portfolio');
  return handleResponse<PortfolioResponse>(response);
};

export const fetchOrders = async (): Promise<OrdersResponse> => {
  const response = await fetch('/api/orders');
  return handleResponse<OrdersResponse>(response);
};

export const submitOrder = async (payload: OrderTicketInput): Promise<Order> => {
  const response = await fetch('/api/orders', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  return handleResponse<Order>(response);
};
