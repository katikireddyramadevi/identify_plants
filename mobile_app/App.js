import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, SafeAreaView } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import HomeScreen from './src/screens/HomeScreen';
import PredictionScreen from './src/screens/PredictionScreen';
import { COLORS } from './src/styles/theme';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState('Login');
  const [user, setUser] = useState(null);

  const navigate = (screen) => setCurrentScreen(screen);

  const renderScreen = () => {
    switch (currentScreen) {
      case 'Login':
        return <LoginScreen onNavigate={navigate} onLoginSuccess={(u) => { setUser(u); navigate('Home'); }} />;
      case 'Register':
        return <RegisterScreen onNavigate={navigate} />;
      case 'Home':
        return <HomeScreen onNavigate={navigate} user={user} onLogout={() => { setUser(null); navigate('Login'); }} />;
      case 'Prediction':
        return <PredictionScreen onNavigate={navigate} />;
      default:
        return <LoginScreen onNavigate={navigate} />;
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" backgroundColor={COLORS.forest} />
      {renderScreen()}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.cream,
  },
});
