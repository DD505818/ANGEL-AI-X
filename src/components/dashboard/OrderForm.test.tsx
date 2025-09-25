import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi, beforeEach } from 'vitest';
import OrderForm from './OrderForm';
import type { PortfolioResponse } from '../../types/trading';
import { submitOrder } from '../../lib/api';

vi.mock('../../lib/api', () => ({
  submitOrder: vi.fn().mockResolvedValue({ id: 'ord-test' }),
}));

const mockPortfolio: PortfolioResponse = {
  metrics: {
    nav: 1_000_000,
    var95: 10_000,
    expectedShortfall: 15_000,
    maxDrawdown: 0.1,
    leverage: 2,
    kellyFraction: 0.2,
    availableBuyingPower: 100_000,
  },
  positions: [],
  exposures: [],
  equityCurve: [],
  returns: [],
  limits: {
    maxLeverage: 3,
    maxDrawdown: 0.2,
    perTradeVaR: 12_000,
  },
  generatedAt: new Date().toISOString(),
};

describe('OrderForm', () => {
  const mockedSubmitOrder = vi.mocked(submitOrder);

  beforeEach(() => {
    mockedSubmitOrder.mockClear();
  });

  it('validates against buying power', async () => {
    render(<OrderForm portfolio={mockPortfolio} onSubmitted={() => {}} />);
    const quantityInput = screen.getByLabelText(/quantity/i);
    fireEvent.change(quantityInput, { target: { value: '1000' } });
    const button = screen.getByRole('button', { name: /route order/i });
    fireEvent.click(button);
    await waitFor(() => {
      expect(screen.getByText(/buying power/i)).toBeInTheDocument();
    });
    expect(mockedSubmitOrder).not.toHaveBeenCalled();
  });
});
