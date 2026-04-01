const BASE_URL = 'http://172.19.22.190:8000'; // Updated to match current system IP: 172.19.22.190

export const api = {
  login: async (loginid, password) => {
    const response = await fetch(`${BASE_URL}/api/mobile/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ loginid, password }),
    });
    return response.json();
  },
  register: async (data) => {
    const response = await fetch(`${BASE_URL}/api/mobile/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  predict: async (imageUri) => {
    const formData = new FormData();
    formData.append('image', {
      uri: imageUri,
      name: 'photo.jpg',
      type: 'image/jpeg',
    });

    const response = await fetch(`${BASE_URL}/api/mobile/predict/`, {
      method: 'POST',
      headers: { 'Content-Type': 'multipart/form-data' },
      body: formData,
    });
    return response.json();
  },
};
