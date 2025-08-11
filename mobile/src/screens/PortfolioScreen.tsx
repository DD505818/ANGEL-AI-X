/**
 * PortfolioScreen visualizes asset allocations and performance.
 */
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import GlassCard from '../components/GlassCard';

export default function PortfolioScreen(): React.JSX.Element {
  return (
    <View style={styles.container}>
      <GlassCard>
        <Text style={styles.text}>Portfolio visualization coming soon.</Text>
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
  text: {
    color: '#fff',
  },
});
