/**
 * Wallet Manager widget showing account balance.
 */
import React from 'react';

export const WalletManager: React.FC<{ balance: number; currency: string }> = ({ balance, currency }) => (
  <div className="p-2">
    <h3 className="font-bold">Balance</h3>
    <p>
      {currency} {balance.toFixed(2)}
    </p>
  </div>
);
