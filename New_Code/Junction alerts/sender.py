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
    {'car': 'Car1', 'lat': 10.903692, 'lon': 76.899055, 'speed': 50},
    {'car': 'Car1', 'lat': 10.903688, 'lon': 76.899016, 'speed': 50},
    {'car': 'Car1', 'lat': 10.903678, 'lon': 76.898964, 'speed': 50},
    {'car': 'Car1', 'lat': 10.903674, 'lon': 76.898928, 'speed': 50},
    {'car': 'Car1', 'lat': 10.903672, 'lon': 76.898892, 'speed': 50},
    {'car': 'Car2', 'lat': 10.903839, 'lon': 76.898829, 'speed': 30},
    {'car': 'Car2', 'lat': 10.903805, 'lon': 76.898833, 'speed': 30},
    {'car': 'Car2', 'lat': 10.903767, 'lon': 76.898842, 'speed': 30},
    {'car': 'Car2', 'lat': 10.903711, 'lon': 76.898841, 'speed': 30},
    {'car': 'Car2', 'lat': 10.903684, 'lon': 76.898845, 'speed': 30},
    {'car': 'Car3', 'lat': 10.903504, 'lon': 76.898857, 'speed': 40},
    {'car': 'Car3', 'lat': 10.903542, 'lon': 76.898853, 'speed': 40},
    {'car': 'Car3', 'lat': 10.903577, 'lon': 76.898850, 'speed': 40},
    {'car': 'Car3', 'lat': 10.903605, 'lon': 76.898846, 'speed': 40},
    {'car': 'Car3', 'lat': 10.903637, 'lon': 76.898849, 'speed': 40}
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
