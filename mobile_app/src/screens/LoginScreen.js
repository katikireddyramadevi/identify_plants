import React, { useState } from 'react';
import { StyleSheet, View, Text, TextInput, TouchableOpacity, Alert, Image } from 'react-native';
import { COLORS } from '../styles/theme';
import { api } from '../api';

const LoginScreen = ({ onNavigate, onLoginSuccess }) => {
  const [loginid, setLoginid] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    if (!loginid || !password) {
      Alert.alert('Error', 'Please enter login ID and password');
      return;
    }
    try {
      const res = await api.login(loginid, password);
      if (res.status === 'success') {
        onLoginSuccess(res.user);
      } else {
        Alert.alert('Error', res.message || 'Login failed');
      }
    } catch (e) {
      Alert.alert('Error', 'Could not connect to server: ' + e.message);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.icon}>🌿</Text>
        <Text style={styles.title}>HerbalVision AI</Text>
        <Text style={styles.sub}>Deep Learning · Medicinal Plants</Text>
      </View>

      <View style={styles.form}>
        <Text style={styles.label}>Login ID</Text>
        <TextInput 
          style={styles.input} 
          placeholder="Enter login ID"
          value={loginid}
          onChangeText={setLoginid}
          autoCapitalize="none"
        />
        
        <Text style={styles.label}>Password</Text>
        <TextInput 
          style={styles.input} 
          placeholder="Enter password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <TouchableOpacity style={styles.loginBtn} onPress={handleLogin}>
          <Text style={styles.loginBtnText}>LOGIN</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => onNavigate('Register')}>
          <Text style={styles.footerText}>Don't have an account? <Text style={styles.link}>REGISTER</Text></Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.cream, padding: 20 },
  header: { alignItems: 'center', marginTop: 80, marginBottom: 50 },
  icon: { fontSize: 50 },
  title: { fontSize: 24, fontWeight: 'bold', color: COLORS.forest, letterSpacing: 1 },
  sub: { fontSize: 12, color: COLORS.sage, textTransform: 'uppercase', letterSpacing: 2 },
  form: { backgroundColor: COLORS.white, padding: 25, borderRadius: 20, elevation: 10, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.1, shadowRadius: 10 },
  label: { fontSize: 13, color: COLORS.forest, marginBottom: 8, fontWeight: '500' },
  input: { backgroundColor: COLORS.cream, padding: 12, borderRadius: 10, marginBottom: 20, borderColor: COLORS.parchment, borderWidth: 1 },
  loginBtn: { backgroundColor: COLORS.gold, padding: 15, borderRadius: 30, alignItems: 'center', marginTop: 10 },
  loginBtnText: { color: COLORS.forest, fontWeight: 'bold', letterSpacing: 1 },
  footerText: { textAlign: 'center', marginTop: 25, color: COLORS.sage, fontSize: 13 },
  link: { color: COLORS.gold, fontWeight: 'bold' },
});

export default LoginScreen;
