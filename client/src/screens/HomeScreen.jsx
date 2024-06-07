import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity,Button } from 'react-native';
import Animated, { useSharedValue, useAnimatedStyle, withRepeat, withTiming } from 'react-native-reanimated';


const HomeScreen = ({ navigation }) => {
  const offset = useSharedValue(0);

  const animatedStyles = useAnimatedStyle(() => {
    return {
      transform: [{ translateY: withRepeat(withTiming(offset.value, { duration: 1000 }), -1, true) }],
    };
  });

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Aldea CHAT</Text>
      <Text style={styles.subtitle}>CHAT APP & MESSAGE</Text>
      <Button title="Go to Login" onPress={() => navigation.navigate('Login')} />
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Log In</Text>
      </TouchableOpacity>
      <Animated.View style={[styles.wave, animatedStyles]} />
    </View>
  );
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 50,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'teal',
  },
  subtitle: {
    fontSize: 18,
    color: '#333',
    marginVertical: 10,
  },
  button: {
    backgroundColor: 'teal',
    padding: 10,
    borderRadius: 5,
    marginTop: 20,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
  },
  wave: {
    width: '100%',
    height: 50,
    backgroundColor: 'cyan',
    position: 'absolute',
    bottom: 0,
  },
});

export default HomeScreen;
