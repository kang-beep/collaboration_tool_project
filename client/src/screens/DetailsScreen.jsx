import React from 'react';
import { View, Text, Button } from 'react-native';

const DetailsScreen = ({ goToHome }) => {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Details Screen</Text>
      <Button title="Back to Home" onPress={goToHome} />
    </View>
  );
};

export default DetailsScreen;
