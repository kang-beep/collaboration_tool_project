import React, { useState } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import axios from 'axios';
import Navbar from 'components/Navbar';

function HomeScreen({ navigation }) {
  const [text, setText] = useState("없음");
  
  const clicked = () => {
    axios.get("http://10.0.2.2:8000/chat/test", {
      params: {
        abc: "가나다",
      }
    })
    .then(response => setText(JSON.stringify(response.data)))
    .catch(error => {
      console.error("Error fetching data: ", error);
      setText("Failed to fetch data");
    });
  };

  return (
    <View style={styles.container}>
        <Navbar navigation={navigation} />

        <Text style={styles.header}>{text}</Text>
        <Button title="클릭" onPress={clicked} />
      
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10
  },
  header: {
    fontSize: 24,
    marginBottom: 20,
  }
});

export default HomeScreen;
