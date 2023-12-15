import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Login from './app/screens/Login';
import Display from './app/screens/Display';
import Map from './app/screens/Map';
import { onAuthStateChanged } from 'firebase/auth'
import React, { useState, useEffect } from "react";
import { FIREBASE_AUTH } from './firebaseConfig';


const Stack = createNativeStackNavigator();

export default function App({ navigation }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    onAuthStateChanged(FIREBASE_AUTH, (user) => {
      setUser(user); 
    })
  }, [])
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName='Login'>
        <Stack.Screen name='Login' component={Login} options={{ headerShown: false }} />
        <Stack.Screen name="Display" component={Display} options={{ headerShown: false }} />
        <Stack.Screen name="Map" component={Map} options={{ headerShown: false }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

