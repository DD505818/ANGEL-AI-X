import { render, screen } from '@testing-library/react';
import Home from './page';

test('renders tagline', () => {
  render(<Home />);
  expect(screen.getByText('Divine Execution. Extreme Profits.')).toBeInTheDocument();
});
