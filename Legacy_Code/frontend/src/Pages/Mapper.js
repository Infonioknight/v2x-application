import React, { useRef, useEffect, useState } from 'react';
import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import './Mapper.css';

mapboxgl.accessToken = 'pk.eyJ1IjoiaW5mb25pb2tuaWdodCIsImEiOiJjbHB6cW5kMmgxYXN0MmtzODZmY2F6MHhtIn0.ZPGrhU1K_3PMoX6OA1B5qw';

const Mapper = (props) => {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [entry, setEntry] = useState(0)
  const [lng, setLng] = useState(props.coords[0].longitude || 76.192034);
  const [lat, setLat] = useState(props.coords[0].latitude || 10.928631);
  // const [speed, setSpeed] = useState(props.coords[0].speed || 10)
  const speed = 0;
  const zoom = 15;

  const mapRender = () => {
    if (map.current) 
      map.current = null;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/outdoors-v12',
      center: [lng, lat],
      zoom: zoom,
    });

    // Add a marker at the specified location
    new mapboxgl.Marker().setLngLat([lng, lat]).addTo(map.current);
  }

  useEffect(() => {
    mapRender(); // eslint-disable-next-line 
  }, [entry]);

  useEffect(() => {
    if(entry === 0) {
      setLat(props.coords[entry].latitude)
      setLng(props.coords[entry].longitude)
      // setSpeed(props.coords[entry].speed)
      mapRender();
    }
    else
      setEntry(entry + 1)  // eslint-disable-next-line 
  }, [props.coords.length])


  const locPrev = () => {
    if(entry !== 0) {
      setEntry(entry - 1);
      setLat(props.coords[entry].latitude)
      setLng(props.coords[entry].longitude)
    }
  }

  const locNext = () => {
    if(entry !== props.coords.length-1)
      setEntry(entry + 1)
      setLat(props.coords[entry].latitude)
      setLng(props.coords[entry].longitude)
  }

  return (
    <div>
      <div className={`${speed > 50 && entry === 0 ? "alert" : "safe"} ${speed > 50 && speed < 70 ? "warning" : ""} ${speed > 70 ? "danger" : ""}`}>
        <h1 className="main-warning">{speed > 50 && speed < 70 ? "Caution: Speeding Up" : "Danger!"}</h1>
        <h5 className="advice">{speed > 50 && speed < 70 ? "Slow down to avoid danger." : "Slow down immediately to avoid accidents!"}</h5>
        <h4 className="speed">Speed: {speed}</h4>
      </div>
      <div className="sidebar">
        <button className={`pagination ${entry === 0 ? "end" : ""} left`} onClick={locPrev}>{entry === 0 ? 'No Newer' : 'Newer'}</button>
        <button className={`pagination ${entry === props.coords.length-1 ? "end" : ""} right`} onClick={locNext}>{entry === props.coords.length-1 ? 'No Older' : 'Older'}</button>
      </div>
      <div className={`${entry === 0 && props.coords[entry].hotspot ? "hotspot" : "safe"}`}>
        <h3 className="hotspot-text">Stay Alert! Collision-prone zone</h3>
      </div>
      <div ref={mapContainer} className="map-container" />
    </div>
  );
};

export default Mapper;
