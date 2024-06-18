import React from 'react';
import StackNavigation from './navigation/StackNavigation';
import { NavigationContainer } from '@react-navigation/native';
import DrawerNavigator from './navigation/DrawerNavigator';
import 'react-native-gesture-handler'

export default function App() {
  return (
    <NavigationContainer>
      <DrawerNavigator />
    </NavigationContainer>
    
  );
}