/**
 * DashboardScreen displays trading widgets and live market data.
 */
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import GlassCard from '../components/GlassCard';
import useMarketData from '../hooks/useMarketData';
import { useRiskStore } from '../store/useRiskStore';

export default function DashboardScreen(): React.JSX.Element {
  const price = useMarketData();
  const { killSwitch, toggleKillSwitch } = useRiskStore();

  return (
    <View style={styles.container}>
      <GlassCard style={styles.widget}>
        <Text style={styles.label}>BTC/USD</Text>
        <Text style={styles.value}>{price.toFixed(2)}</Text>
      </GlassCard>
      <GlassCard style={styles.widget}>
        <Text style={styles.label}>Kill Switch: {killSwitch ? 'ON' : 'OFF'}</Text>
        <Text style={styles.link} onPress={toggleKillSwitch}>
          Toggle
        </Text>
      </GlassCard>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    padding: 16,
  },
  widget: { marginBottom: 16 },
  label: { color: '#0ff', marginBottom: 4 },
  value: { color: '#fff', fontSize: 20 },
  link: { color: '#a0a0ff', marginTop: 8 },
});
