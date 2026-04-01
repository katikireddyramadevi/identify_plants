import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { COLORS } from '../styles/theme';

const HomeScreen = ({ onNavigate, user, onLogout }) => {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.welcome}>Welcome,</Text>
        <Text style={styles.username}>{user?.name || 'User'}</Text>
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Identify Plant</Text>
          <Text style={styles.cardDesc}>Upload a leaf image to identify its medicinal properties using our AI model.</Text>
          <TouchableOpacity 
            style={styles.actionBtn} 
            onPress={() => onNavigate('Prediction')}
          >
            <Text style={styles.actionBtnText}>ANALYZE NOW</Text>
          </TouchableOpacity>
        </View>

        <View style={[styles.card, { backgroundColor: COLORS.parchment }]}>
          <Text style={styles.cardTitle}>Model Training Info</Text>
          <Text style={styles.cardDesc}>Our model uses MobileNet and CNN architectures for high accuracy.</Text>
          <View style={styles.stats}>
            <View style={styles.stat}>
              <Text style={styles.statVal}>89%</Text>
              <Text style={styles.statLab}>Accuracy</Text>
            </View>
            <View style={styles.stat}>
              <Text style={styles.statVal}>1000+</Text>
              <Text style={styles.statLab}>Dataset</Text>
            </View>
          </View>
        </View>

        <TouchableOpacity style={styles.logoutBtn} onPress={onLogout}>
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.cream },
  header: { backgroundColor: COLORS.forest, padding: 30, paddingBottom: 50, borderBottomLeftRadius: 30, borderBottomRightRadius: 30 },
  welcome: { color: COLORS.mist, fontSize: 16 },
  username: { color: COLORS.amber, fontSize: 28, fontWeight: 'bold' },
  content: { padding: 20 },
  card: { backgroundColor: COLORS.white, padding: 25, borderRadius: 20, marginBottom: 20, elevation: 4 },
  cardTitle: { fontSize: 18, fontWeight: 'bold', color: COLORS.forest, marginBottom: 10 },
  cardDesc: { color: COLORS.sage, fontSize: 14, lineHeight: 20, marginBottom: 20 },
  actionBtn: { backgroundColor: COLORS.gold, padding: 15, borderRadius: 30, alignItems: 'center' },
  actionBtnText: { color: COLORS.forest, fontWeight: 'bold' },
  stats: { flexDirection: 'row', justifyContent: 'space-around', marginTop: 10 },
  stat: { alignItems: 'center' },
  statVal: { fontSize: 20, fontWeight: 'bold', color: COLORS.bark },
  statLab: { fontSize: 11, color: COLORS.sage, textTransform: 'uppercase' },
  logoutBtn: { padding: 15, alignItems: 'center', marginTop: 10 },
  logoutText: { color: COLORS.error, fontWeight: '500' },
});

export default HomeScreen;
