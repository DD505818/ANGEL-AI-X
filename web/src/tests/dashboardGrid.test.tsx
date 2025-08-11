import React from 'react';
import { render, screen } from '@testing-library/react';
import { DashboardGrid } from '../components/DashboardGrid';

jest.mock('../lib/firebase', () => ({ db: {} }));
jest.mock('firebase/firestore', () => ({
  doc: jest.fn(),
  getDoc: jest.fn(() => Promise.resolve({ exists: () => false })),
  setDoc: jest.fn(() => Promise.resolve()),
}));

test('renders default widgets', async () => {
  render(<DashboardGrid userId="user" />);
  expect(await screen.findByText(/Portfolio Value/)).toBeInTheDocument();
});
