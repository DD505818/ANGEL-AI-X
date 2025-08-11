import React from 'react';
import { render, screen } from '@testing-library/react';
import { OnboardingModal } from '../components/OnboardingModal';

test('renders children when open', () => {
  render(<OnboardingModal isOpen onClose={() => {}}>hello</OnboardingModal>);
  expect(screen.getByText('hello')).toBeInTheDocument();
});
