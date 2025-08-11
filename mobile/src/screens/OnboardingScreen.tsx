/**
 * OnboardingScreen guides new users through initial setup.
 */
import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import GlassCard from '../components/GlassCard';

export interface OnboardingProps {
  onFinish: () => void;
}

export default function OnboardingScreen({ onFinish }: OnboardingProps): React.JSX.Element {
  return (
    <View style={styles.container}>
      <GlassCard>
        <Text style={styles.title}>ANGEL.AI</Text>
        <Text style={styles.tagline}>Divine Execution. Extreme Profits.</Text>
        <Button title="Enter" onPress={onFinish} />
      </GlassCard>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#000',
  },
  title: {
    fontSize: 24,
    color: '#0ff',
    marginBottom: 8,
    textAlign: 'center',
  },
  tagline: {
    fontSize: 12,
    color: '#a0a0ff',
    marginBottom: 16,
    textAlign: 'center',
  },
});
