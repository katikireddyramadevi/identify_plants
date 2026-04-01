import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Image, ScrollView, ActivityIndicator, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { COLORS } from '../styles/theme';
import { api } from '../api';

const PredictionScreen = ({ onNavigate }) => {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const pickImage = async () => {
    let res = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 1,
    });

    if (!res.canceled) {
      setImage(res.assets[0].uri);
      setResult(null);
    }
  };

  const handlePredict = async () => {
    if (!image) return;
    setLoading(true);
    try {
      const res = await api.predict(image);
      if (res.status === 'success') {
        setResult(res);
      } else {
        Alert.alert('Error', res.message);
      }
    } catch (e) {
      Alert.alert('Error', 'Prediction failed: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.nav}>
        <TouchableOpacity onPress={() => onNavigate('Home')}>
          <Text style={styles.backBtn}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.navTitle}>Herbal Analysis</Text>
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.imageBox}>
          {image ? (
            <Image source={{ uri: image }} style={styles.preview} />
          ) : (
            <View style={styles.placeholder}>
              <Text style={styles.placeholderText}>No image selected</Text>
            </View>
          )}
        </View>

        <TouchableOpacity style={styles.pickBtn} onPress={pickImage}>
          <Text style={styles.pickBtnText}>SELECT LEAF IMAGE</Text>
        </TouchableOpacity>

        {image && !result && (
          <TouchableOpacity 
            style={[styles.predictBtn, loading && { opacity: 0.7 }]} 
            onPress={handlePredict}
            disabled={loading}
          >
            {loading ? <ActivityIndicator color="white" /> : <Text style={styles.predictBtnText}>ANALYZE PLANT</Text>}
          </TouchableOpacity>
        )}

        {result && (
          <View style={styles.resultCard}>
            <Text style={styles.resultLabel}>Identified Plant:</Text>
            <Text style={styles.resultVal}>{result.predicted_class}</Text>
            <View style={styles.divider} />
            <Text style={styles.descLabel}>Medicinal Properties:</Text>
            <Text style={styles.descVal}>{result.description}</Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.cream },
  nav: { backgroundColor: COLORS.forest, height: 100, flexDirection: 'row', alignItems: 'flex-end', padding: 20, paddingBottom: 15 },
  backBtn: { color: COLORS.amber, fontWeight: 'bold', fontSize: 16 },
  navTitle: { color: COLORS.white, fontSize: 18, fontWeight: 'bold', marginLeft: 20 },
  content: { padding: 20, alignItems: 'center' },
  imageBox: { width: '100%', height: 250, backgroundColor: COLORS.white, borderRadius: 20, overflow: 'hidden', marginBottom: 20, elevation: 5 },
  preview: { width: '100%', height: '100%' },
  placeholder: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  placeholderText: { color: COLORS.mist, fontStyle: 'italic' },
  pickBtn: { backgroundColor: COLORS.sage, padding: 15, borderRadius: 30, width: '100%', alignItems: 'center', marginBottom: 15 },
  pickBtnText: { color: 'white', fontWeight: 'bold' },
  predictBtn: { backgroundColor: COLORS.gold, padding: 15, borderRadius: 30, width: '100%', alignItems: 'center', marginBottom: 15 },
  predictBtnText: { color: COLORS.forest, fontWeight: 'bold' },
  resultCard: { backgroundColor: COLORS.white, padding: 25, borderRadius: 20, width: '100%', elevation: 5, marginTop: 10 },
  resultLabel: { color: COLORS.sage, fontSize: 12, textTransform: 'uppercase', marginBottom: 5 },
  resultVal: { color: COLORS.forest, fontSize: 24, fontWeight: 'bold', marginBottom: 15 },
  divider: { height: 1, backgroundColor: COLORS.parchment, marginBottom: 15 },
  descLabel: { color: COLORS.sage, fontSize: 12, textTransform: 'uppercase', marginBottom: 5 },
  descVal: { color: COLORS.bark, fontSize: 15, lineHeight: 22 },
});

export default PredictionScreen;
