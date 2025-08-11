import '../styles/globals.css';
import { Inter, Space_Grotesk, JetBrains_Mono } from 'next/font/google';
import type { ReactNode } from 'react';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const space = Space_Grotesk({ subsets: ['latin'], variable: '--font-space' });
const mono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' });

export const metadata = {
  title: 'ANGEL.AI',
  description: 'Divine Execution. Extreme Profits.',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${space.variable} ${mono.variable}`}>
      <body className="bg-dark text-white">{children}</body>
    </html>
  );
}
