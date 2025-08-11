/**
 * Entry point for the ANGEL.AI mobile trading application.
 */
import React, { useState } from 'react';
import { SafeAreaView } from 'react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import OnboardingScreen from './src/screens/OnboardingScreen';
import DashboardScreen from './src/screens/DashboardScreen';

const queryClient = new QueryClient();

export default function App(): React.JSX.Element {
  const [complete, setComplete] = useState(false);

  return (
    <QueryClientProvider client={queryClient}>
      <SafeAreaView style={{ flex: 1 }}>
        {complete ? (
          <DashboardScreen />
        ) : (
          <OnboardingScreen onFinish={() => setComplete(true)} />
        )}
      </SafeAreaView>
    </QueryClientProvider>
  );
}
