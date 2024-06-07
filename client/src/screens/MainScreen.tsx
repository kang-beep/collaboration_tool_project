import React from 'react';
import { View, Text, Button } from 'react-native';

const MainScreen = ({ navigation }) => {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Home</Text>
      <Button title="Drawer 열기" onPress={() => navigation.openDrawer()} />
      <Button title="chat 열기" onPress={() => navigation.navigate('Chat')} />
      <Button title="캘린더 열기" onPress={() => navigation.navigate('Calendar')} />
    </View>
  );
};

export default MainScreen;
