// LoginScreen.js
import React, { useState } from 'react';
import { View, TextInput, Button, AsyncStorage } from 'react-native';
import axios from 'axios';

const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://10.0.2.2:8000/api/token/', {
        username,
        password,
      });
      const { access, refresh } = response.data;
      await AsyncStorage.setItem('accessToken', access);
      await AsyncStorage.setItem('refreshToken', refresh);
      alert('Login successful!');
    } catch (error) {
      alert('Failed to log in!');
      console.error(error);
    }
  };

  return (
    <View>
      <TextInput
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Log In" onPress={handleLogin} />
    </View>
  );
};

export default LoginScreen;
