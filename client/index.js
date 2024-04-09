/**
 * @format
 */

import React, { useState } from 'react';
import { AppRegistry, StyleSheet, View, Text, Button }  from 'react-native'; // Add View and Text to the import
import axios from "axios";


// App 컴포넌트 정의
const App = () => {
  const [text, setText] = useState("없음");

  const clicked = () => {
    axios
      .get("http://10.0.2.2:8000/chat/test", {
        params: {
          abc: "가나다",
        },
      })
      .then((response) => setText(JSON.stringify(response.data)));
  };


  return (
    <View style={styles.container}>
      <Text>{text}</Text>
      <Button title="클릭" onPress={clicked} />
    </View>
  );
};

// 스타일 시트 생성
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
// App 컴포넌트를 앱의 메인 컴포넌트로 등록
AppRegistry.registerComponent('client', () => App);
