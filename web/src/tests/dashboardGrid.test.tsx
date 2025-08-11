import React from 'react';
import { render, screen } from '@testing-library/react';
import { vi } from 'vitest';
import { DashboardGrid } from '../components/DashboardGrid';

vi.mock('../lib/firebase', () => ({ db: {} }));
vi.mock('firebase/firestore', () => ({
  doc: vi.fn(),
  getDoc: vi.fn(() => Promise.resolve({ exists: () => false })),
  setDoc: vi.fn(() => Promise.resolve()),
}));

test('renders default widgets', async () => {
  render(<DashboardGrid userId="user" />);
  expect(await screen.findByText(/Portfolio Value/)).toBeInTheDocument();
});
