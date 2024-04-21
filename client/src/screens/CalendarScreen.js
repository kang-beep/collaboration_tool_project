import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { Calendar } from 'react-native-calendars';
import Navbar from '../components/Navbar'; // 경로 확인 필요

export default function CalendarPage({ navigation }) {
  // 일정 데이터를 상태로 관리
  const [markedDates, setMarkedDates] = React.useState({
    '2023-04-15': {selected: true, marked: true, selectedColor: 'blue'},
    '2023-04-20': {marked: true, dotColor: 'red'},
    '2023-04-22': {marked: true, dotColor: 'green', activeOpacity: 0},
  });

  // 일정 추가 함수
  const addEvent = (date) => {
    const newDates = {...markedDates};
    newDates[date] = {marked: true, dotColor: 'purple'};
    setMarkedDates(newDates);
  };

  return (
    <View>
      <Navbar navigation={navigation} />
      <Text style={styles.header}>Calendar</Text>
      <Calendar
        onDayPress={(day) => {
          console.log('selected day', day.dateString);
          addEvent(day.dateString); // 날짜 클릭 시 이벤트 추가
        }}
        markedDates={markedDates}
      />
      
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  header: {
    fontSize: 24,
    marginBottom: 20,
  },
});
