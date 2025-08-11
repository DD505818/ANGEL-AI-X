import Image from 'next/image';

/**
 * Home page rendering ANGEL.AI branding.
 */
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4">
      <Image src="/halo.svg" alt="ANGEL.AI logo" width={80} height={80} />
      <h1 className="font-space text-4xl">ANGEL.AI</h1>
      <p className="font-inter">Divine Execution. Extreme Profits.</p>
    </main>
  );
}
