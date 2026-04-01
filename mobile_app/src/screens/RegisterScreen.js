import React, { useState } from 'react';
import { StyleSheet, View, Text, TextInput, TouchableOpacity, Alert, ScrollView } from 'react-native';
import { COLORS } from '../styles/theme';
import { api } from '../api';

const RegisterScreen = ({ onNavigate }) => {
  const [form, setForm] = useState({
    name: '', loginid: '', password: '', mobile: '', email: '',
    locality: '', address: '', city: '', state: ''
  });

  const handleRegister = async () => {
    if (!form.loginid || !form.password || !form.email) {
      Alert.alert('Error', 'Please fill mandatory fields');
      return;
    }
    try {
      const res = await api.register(form);
      if (res.status === 'success') {
        Alert.alert('Success', 'Registration successful! Wait for admin activation.', [
          { text: 'OK', onPress: () => onNavigate('Login') }
        ]);
      } else {
        Alert.alert('Error', res.message);
      }
    } catch (e) {
      Alert.alert('Error', 'Connection failed');
    }
  };

  const updateForm = (key, val) => setForm({ ...form, [key]: val });

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Create Account</Text>
      <View style={styles.form}>
        <TextInput style={styles.input} placeholder="Full Name" onChangeText={v => updateForm('name', v)} />
        <TextInput style={styles.input} placeholder="Login ID" onChangeText={v => updateForm('loginid', v)} />
        <TextInput style={styles.input} placeholder="Password" secureTextEntry onChangeText={v => updateForm('password', v)} />
        <TextInput style={styles.input} placeholder="Mobile" keyboardType="phone-pad" onChangeText={v => updateForm('mobile', v)} />
        <TextInput style={styles.input} placeholder="Email" keyboardType="email-address" onChangeText={v => updateForm('email', v)} />
        <TextInput style={styles.input} placeholder="City" onChangeText={v => updateForm('city', v)} />
        
        <TouchableOpacity style={styles.regBtn} onPress={handleRegister}>
          <Text style={styles.regBtnText}>REGISTER</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => onNavigate('Login')}>
          <Text style={styles.footerText}>Already have an account? <Text style={styles.link}>LOGIN</Text></Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.cream, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: COLORS.forest, marginTop: 40, marginBottom: 30, textAlign: 'center' },
  form: { backgroundColor: COLORS.white, padding: 20, borderRadius: 20, marginBottom: 50 },
  input: { backgroundColor: COLORS.cream, padding: 12, borderRadius: 10, marginBottom: 15, borderColor: COLORS.parchment, borderWidth: 1 },
  regBtn: { backgroundColor: COLORS.sage, padding: 15, borderRadius: 30, alignItems: 'center', marginTop: 10 },
  regBtnText: { color: 'white', fontWeight: 'bold' },
  footerText: { textAlign: 'center', marginTop: 20, color: COLORS.sage },
  link: { color: COLORS.gold, fontWeight: 'bold' },
});

export default RegisterScreen;
