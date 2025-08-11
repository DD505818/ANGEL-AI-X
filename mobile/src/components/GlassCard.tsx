/**
 * GlassCard renders content with a glassmorphism style.
 */
import React from 'react';
import { View, StyleSheet, ViewProps } from 'react-native';

export default function GlassCard({ children, style }: React.PropsWithChildren<ViewProps>): React.JSX.Element {
  return <View style={[styles.card, style]}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderColor: 'rgba(255, 255, 255, 0.3)',
    borderWidth: 1,
    borderRadius: 16,
    padding: 16,
  },
});
