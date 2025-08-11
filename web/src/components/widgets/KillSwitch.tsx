/**
 * Kill Switch widget to disable trading immediately.
 */
import React, { useState } from 'react';
import { motion } from 'framer-motion';

export const KillSwitch: React.FC = () => {
  const [enabled, setEnabled] = useState(true);
  return (
    <motion.button
      whileTap={{ scale: 0.95 }}
      onClick={() => setEnabled(false)}
      disabled={!enabled}
      className={`p-2 rounded ${enabled ? 'bg-red-600 text-white' : 'bg-gray-400 text-black'}`}
    >
      {enabled ? 'Disable Trading' : 'Trading Disabled'}
    </motion.button>
  );
};
