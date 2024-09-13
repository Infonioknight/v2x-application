import paho.mqtt.client as mqtt
import json
import time

# Define the MQTT broker address and port
broker_address = "127.0.0.1"
broker_port = 1883

# Define the topic to which you want to publish the data
topic = "Vehicledata"

# Define the data to be published
data = [
    {'car': 'Car1', 'lat': 10.903817, 'lon': 76.903611, 'speed': 50},
    {'car': 'Car1', 'lat': 10.903817, 'lon': 76.903616, 'speed': 50},
    {'car': 'Car1', 'lat': 10.903819, 'lon': 76.903628, 'speed': 50},
    {'car': 'Car1', 'lat': 10.903818, 'lon': 76.903643, 'speed': 50},
    {'car': 'Car1', 'lat': 10.903817, 'lon': 76.903658, 'speed': 50},
    {'car': 'Car2', 'lat': 10.903599, 'lon': 76.903965, 'speed': 40},
    {'car': 'Car2', 'lat': 10.903624, 'lon': 76.903965, 'speed': 40},
    {'car': 'Car2', 'lat': 10.903630, 'lon': 76.903964, 'speed': 40},
    {'car': 'Car2', 'lat': 10.903638, 'lon': 76.903964, 'speed': 40},
    {'car': 'Car2', 'lat': 10.903645, 'lon': 76.903964, 'speed': 40}
]

# Define a shared variable to keep track of the number of messages received by the receiver
received_messages = 0

# Callback function to handle connection status
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code:", rc)

# Callback function to handle publish result
def on_publish(client, userdata, mid):
    print("Message published with message ID:", mid)
    # Here you can send any confirmation message you like

# Callback function to handle message receipt acknowledgment
def on_message_ack(client, userdata, message):
    global received_messages
    received_messages += 1
    print("Received acknowledgment for message:", message.payload.decode())
    if received_messages == len(data):
        print("All messages received. Exiting...")
        client.disconnect()

# Initialize the MQTT client
client = mqtt.Client()

# Assign the callback functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message_ack

# Connect to the broker
client.connect(broker_address, broker_port)

# Subscribe to the acknowledgment topic
client.subscribe("acknowledgment_topic")

# Loop through the data and publish each entry
for entry in data:
    result, mid = client.publish(topic, json.dumps(entry))
    if result != mqtt.MQTT_ERR_SUCCESS:
        print("Failed to publish message with message ID:", mid)

# Wait for acknowledgment from the receiver before exiting
client.loop_forever()
