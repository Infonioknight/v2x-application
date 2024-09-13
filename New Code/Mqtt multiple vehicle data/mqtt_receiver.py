import paho.mqtt.client as mqtt
import requests
import json
import sqlite3

mqtt_broker_address = "127.0.0.1"
mqtt_broker_port = 1883
database_file = "vehicle_data.db"

# Connect to SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create a table to store vehicle data if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS VehicleData 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                vehicle_type TEXT, 
                latitude REAL, 
                longitude REAL)''')
conn.commit()

def on_message(client, userdata, msg):
    data = msg.payload.decode('utf-8')
    data_parts = data.split(',')
    
    # Ensure the message contains all required parts
    if len(data_parts) == 3:
        vehicle_type, latitude, longitude = data_parts
        try:
            # Insert data into the database
            cursor.execute('''INSERT INTO VehicleData (vehicle_type, latitude, longitude) 
                            VALUES (?, ?, ?)''', (vehicle_type.strip(), float(latitude), float(longitude)))
            conn.commit()
            print("Data successfully stored in the database.")
        except Exception as e:
            print("Error occurred while storing data:", e)

mqtt_client = mqtt.Client("python_script_subscriber1")
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker_address, mqtt_broker_port, 60)
mqtt_client.subscribe("/nodemcu/car1")

mqtt_client.loop_forever()
