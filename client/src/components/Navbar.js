import React from 'react';
import { View, Button, StyleSheet } from 'react-native';

const Navbar = ({ navigation }) => {
    return (
        <View style={styles.navbar}>
            <Button title="Home" onPress={() => navigation.navigate('Home')} />
            <Button title="Calendar" onPress={() => navigation.navigate('Calendar')} />
        </View>
    );
};

const styles = StyleSheet.create({
    navbar: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        paddingVertical: 10,
        backgroundColor: '#eee',
    }
});

export default Navbar;
