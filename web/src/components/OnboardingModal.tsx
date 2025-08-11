/**
 * Onboarding modal with mobile bottom-sheet behavior and framer-motion animations.
 */
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

export const OnboardingModal: React.FC<Props> = ({ isOpen, onClose, children }) => {
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
  const variants = {
    hidden: { y: isMobile ? '100%' : '-50%', opacity: 0 },
    visible: { y: 0, opacity: 1 },
  };
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex bg-black/50"
          onClick={onClose}
          initial="hidden"
          animate="visible"
          exit="hidden"
        >
          <motion.div
            className={`bg-white dark:bg-gray-800 p-4 ${isMobile ? 'mt-auto w-full rounded-t-lg' : 'm-auto rounded-lg'}`}
            variants={variants}
            onClick={(e) => e.stopPropagation()}
          >
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
