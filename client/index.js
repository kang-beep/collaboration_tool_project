import React from 'react';
import { AppRegistry } from 'react-native';
import App from './src/App'; // This imports the App component from App.js
import { name as appName } from './app.json';

AppRegistry.registerComponent(appName, () => App);
