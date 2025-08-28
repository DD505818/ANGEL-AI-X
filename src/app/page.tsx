import dynamic from 'next/dynamic';
import type { FC } from 'react';

/**
 * Home page rendering ANGEL.AI branding.
 */
const HaloLogo = dynamic(() => import('./HaloLogo'), { ssr: false });

const Home: FC = (): JSX.Element => {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4">
      <HaloLogo />
      <h1 className="font-space text-4xl">ANGEL.AI</h1>
      <p className="font-inter">Divine Execution. Extreme Profits.</p>
    </main>
  );
};

export default Home;
