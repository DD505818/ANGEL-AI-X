/**
 * DashboardGrid provides a drag-and-drop grid persisted in Firestore.
 */
import React, { useEffect, useState } from 'react';
import GridLayout, { Layout } from 'react-grid-layout';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { motion } from 'framer-motion';
import { db } from '../lib/firebase';
import {
  PortfolioGlobe,
  AgentArena,
  TunerPanel,
  PnLSparkline,
  TradeJournal,
  WalletManager,
  SignalLog,
  KillSwitch,
} from './widgets';

const widgetComponents = {
  PortfolioGlobe,
  AgentArena,
  TunerPanel,
  PnLSparkline,
  TradeJournal,
  WalletManager,
  SignalLog,
  KillSwitch,
};

const defaultLayout: Layout[] = [
  { i: 'PortfolioGlobe', x: 0, y: 0, w: 3, h: 2 },
  { i: 'AgentArena', x: 3, y: 0, w: 3, h: 2 },
  { i: 'TunerPanel', x: 6, y: 0, w: 3, h: 2 },
  { i: 'PnLSparkline', x: 9, y: 0, w: 3, h: 2 },
  { i: 'TradeJournal', x: 0, y: 2, w: 6, h: 2 },
  { i: 'WalletManager', x: 6, y: 2, w: 3, h: 2 },
  { i: 'SignalLog', x: 9, y: 2, w: 3, h: 2 },
  { i: 'KillSwitch', x: 0, y: 4, w: 12, h: 1 },
];

const defaultProps = {
  PortfolioGlobe: { positions: [] },
  AgentArena: { agents: [] },
  TunerPanel: {},
  PnLSparkline: { data: [10, 20, 30, 40, 50] },
  TradeJournal: { trades: [] },
  WalletManager: { balance: 0, currency: 'USD' },
  SignalLog: { signals: [] },
  KillSwitch: {},
};

interface Props {
  userId: string;
}

export const DashboardGrid: React.FC<Props> = ({ userId }) => {
  const [layout, setLayout] = useState<Layout[]>(defaultLayout);

  useEffect(() => {
    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'dashboards', userId));
        if (snap.exists()) {
          setLayout(snap.data().layout);
        } else {
          await setDoc(doc(db, 'dashboards', userId), { layout: defaultLayout });
        }
      } catch (err) {
        console.error(err);
      }
    };
    load();
  }, [userId]);

  const handleLayoutChange = async (l: Layout[]) => {
    setLayout(l);
    try {
      await setDoc(doc(db, 'dashboards', userId), { layout: l });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <GridLayout
      className="layout"
      layout={layout}
      cols={12}
      rowHeight={30}
      width={1200}
      onLayoutChange={handleLayoutChange}
    >
      {layout.map((item) => {
        const Component = (widgetComponents as any)[item.i];
        const props = (defaultProps as any)[item.i];
        return (
          <div key={item.i} data-grid={item} className="bg-white dark:bg-gray-900">
            <motion.div whileHover={{ scale: 1.02 }} className="h-full w-full p-2 overflow-auto">
              {Component && <Component {...props} />}
            </motion.div>
          </div>
        );
      })}
    </GridLayout>
  );
};
