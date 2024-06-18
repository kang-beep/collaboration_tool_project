import React from 'react';
import { createDrawerNavigator } from "@react-navigation/drawer";
import StackNavigation from "./StackNavigation";

const Drawer = createDrawerNavigator();

const DrawerNavigator = () => {
  return (
    <Drawer.Navigator initialRouteName="Main">
      <Drawer.Screen name="Main" component={StackNavigation} />
      
    </Drawer.Navigator>
  );
}


export default DrawerNavigator;
