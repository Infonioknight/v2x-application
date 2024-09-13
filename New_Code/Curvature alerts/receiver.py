import paho.mqtt.client as mqtt
import json
import sqlite3

# Define the MQTT broker address and port
broker_address = "127.0.0.1"
broker_port = 1883

# Define the topic to subscribe to
topic = "Vehicledata"

# Function to initialize the SQLite database
def initialize_database():
    try:
        conn = sqlite3.connect("vehicle_data1.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS vehicles
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, car TEXT, lat REAL, lon REAL, speed INTEGER)''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print("Error initializing database:", e)

# Function to insert data into the database
def insert_into_database(car, lat, lon, speed):
    try:
        with sqlite3.connect("vehicle_data1.db") as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO vehicles (car, lat, lon, speed) VALUES (?, ?, ?, ?)''', (car, lat, lon, speed))
            conn.commit()
        print("Data inserted into database.")
    except Exception as e:
        print("Error inserting data into database:", e)

# Callback function to handle connection status
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Subscribe to the topic when connected
        client.subscribe(topic)
    else:
        print("Failed to connect, return code:", rc)

# Callback function to handle received messages
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print("Received message:", payload)
    # Extract data from payload if all required fields are present
    if 'car' in payload and 'lat' in payload and 'lon' in payload and 'speed' in payload:
        car = payload['car']
        lat = payload['lat']
        lon = payload['lon']
        speed = payload['speed']
        # Insert data into the database
        insert_into_database(car, lat, lon, speed)
    else:
        print("Incomplete payload. Missing required fields.")

# Initialize the database
initialize_database()

# Initialize the MQTT client
client = mqtt.Client()

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, broker_port)

# Start the loop to process received messages
client.loop_forever()
