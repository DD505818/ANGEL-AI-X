'use client';

import type { FC } from 'react';
import Dashboard from '../components/dashboard/Dashboard';

/**
 * Landing page delegating to the interactive trading dashboard.
 */
const Home: FC = (): JSX.Element => {
  return <Dashboard />;
};

export default Home;
