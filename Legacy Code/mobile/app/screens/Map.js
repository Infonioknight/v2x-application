import React from 'react';
import MapView from 'react-native-maps';
import { Marker } from 'react-native-maps';
import { StyleSheet, View } from 'react-native';

export default function Map({ navigation, route }) {
  return (
    <View style={styles.container}>
      <MapView
        initialRegion={{
            latitude: route.params.props.latitude,
            longitude: route.params.props.longitude,
            latitudeDelta: 0.001222,
            longitudeDelta: 0.000921,
        }}
        style={styles.map}
    >
        <Marker
            coordinate={{latitude: route.params.props.latitude, longitude: route.params.props.longitude }}
            title="Please work"
            description="Hopefully this works"
        />
    </MapView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    width: '100%',
    height: '100%',
  },
});
