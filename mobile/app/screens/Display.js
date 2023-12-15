import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView } from 'react-native'
import React, { useState } from 'react'
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';
import { FIREBASE_DB } from '../../firebaseConfig'
import { ref, onValue } from 'firebase/database';
import { DataTable } from 'react-native-paper';

const Display = ({ navigation, route }) => {
  const insets = useSafeAreaInsets();
  const [access, setAccess] = useState(route.params.access_key.replace('.', ','))
  const [userData, setUserData] = useState([]);
  const [car, setCar] = useState('')
  const [visible, setVisible] = useState(false);
  const [clicks, setClicks] = useState(0)
  const delay = (delayInms) => {
    return new Promise(resolve => setTimeout(resolve, delayInms));
  };

  const retrieveData = async () => {
    const childRef = ref(FIREBASE_DB, `vehicle/${access}/${car}`);
    let data = [];
    onValue(childRef, (snapshot) => {
      data = Object.values(snapshot.val())
      data = data.slice(data.length - 10, data.length)
    });
    const delayTimer = await delay(2000)
    setUserData(data)
    userData.length > 0 ? setVisible(true) : setVisible(false);
    setClicks(clicks + 1);
  }

  const changeMap = () => {
      navigation.navigate("Map", { props: userData[userData.length-1] })
  }


  return (
    <SafeAreaProvider>
      <View style={{...styles.display, paddingTop: insets.top, paddingBottom: insets.bottom, paddingLeft: insets.left,paddingRight: insets.right,}}>
        <TextInput 
          style={{ backgroundColor: '#bbbbbb', padding: 5, borderRadius: 10}}
          value={car} 
          placeholder='Enter Vehicle Number (Caps, no spaces)' 
          onChangeText={(text) => setCar(text)}
        />
        <TouchableOpacity style={styles.button} onPress={retrieveData}>
          { clicks == 0 ? <Text>Retrieve Data</Text> : <Text>Render Data</Text> }
        </TouchableOpacity>
        {clicks == 1 ? (<Text style={{ justifyContent: 'center', padding: 10}}>Data fetch successful. Click again to render</Text>) : null}
        <TouchableOpacity style={styles.button} onPress={changeMap}>
          {clicks >= 2 ? <Text>Show on Map</Text> : <Text>Not just yet...</Text>}
        </TouchableOpacity>
        <ScrollView>
          <ScrollView horizontal={true}>
            {visible ? (<DataTable style={styles.container}> 
              <DataTable.Header style={styles.tableHeader}> 
                <DataTable.Title style={styles.columnAlign}>Latitude</DataTable.Title> 
                <DataTable.Title style={styles.columnAlign}>Longitude</DataTable.Title> 
                <DataTable.Title style={styles.columnAlign}>Altitude</DataTable.Title> 
                <DataTable.Title style={styles.columnAlign}>Speed</DataTable.Title> 
                <DataTable.Title style={styles.columnAlign}>Brake Status</DataTable.Title> 
              </DataTable.Header> 
              {userData.map((entry) => (
                <DataTable.Row key={userData.indexOf(entry)}>
                  <DataTable.Cell style={styles.columnAlign}>{entry.latitude.toFixed(6)}</DataTable.Cell>
                  <DataTable.Cell style={styles.columnAlign}>{entry.longitude.toFixed(6)}</DataTable.Cell>
                  <DataTable.Cell style={styles.columnAlign}>{entry.altitude.toFixed(6)}</DataTable.Cell>
                  <DataTable.Cell style={styles.columnAlign}>{entry.speed}</DataTable.Cell>
                  <DataTable.Cell style={styles.columnAlign}>{entry.brake_status}</DataTable.Cell>
                </DataTable.Row>
              ))}
            </DataTable>) : null}
          </ScrollView>
        </ScrollView> 
      </View>
    </SafeAreaProvider>
  )
}

const styles = StyleSheet.create({
  display: {
    display: 'flex',
    justifyContent: 'space-around',
    alignItems: 'center',
  },

  button: {
    width: 110,
    height: 40,
    backgroundColor: '#aaaaaa',
    borderRadius: 10,
    marginTop: 10,
    justifyContent: 'center',
    alignItems: 'center'
  },

  container: { 
     padding: 15, 
     width: 500
  }, 
  tableHeader: { 
    backgroundColor: '#DCDCDC', 
  }, 

  columnAlign: {
    width: 100
  }
})


export default Display