import paho.mqtt.client as mqtt
import time

mqtt_broker_address = "127.0.0.1"
mqtt_broker_port = 1883

def on_publish(client, userdata, mid):
    print("Message published")

mqtt_client = mqtt.Client("python_script_publisher1")
mqtt_client.on_publish = on_publish

mqtt_client.connect(mqtt_broker_address, mqtt_broker_port, 60)

vehicle_data = [
    "car, 18, 22",
    "car, 18, 25",
    "car, 18, 30",
    "car, 18, 35",
    "bike, 18, 39",
    "car, 6, 22",
    "ambulance, 6, 25",
    "car, 6, 30",
    "car, 6, 35",
    "bike, 6, 39",
    "cab, 12, 22",
    "car, 12, 25",
    "car, 12, 30",
    "bike, 12, 39",
    "bike, 12, 35",
    "car, 38, -18",
    "bike, 38, -12",
    "cab, 38, -6",
    "car, 38, -3",  
    "cab, 38, -12",
    "car, 38, -6",
    "car, 38, -3",
    "car, 30, -3",
    "bike, 30, -18",
    "cab, 30, -12",
    "car, 30, -6",
    "car, 22, -3",
    "car, 22, -12",
    "car, 22, -6",
    "bike, 22, -18",
    "car, -3, -37",
    "car, -3, -30",
    "cab, 3, -12",
    "cab, -3, -26",
    "car, -8, -37",
    "ambulance, -8, -30",
    "cab, -8, -26",
    "car, -15, -37",
    "car, -15, -30",
    "car, -15, -26",
    "cab, 30, -12",
    "car, -23, 8",
    "car, -23, 12",
    "car, -23, 16",
    "car, -27, 8",
    "car, -27, 12",
    "cab, -27, 16",
    "car, -33, 8",
    "car, -33, 12",
    "cab, -33, 16"
]

for data in vehicle_data:
    mqtt_client.publish("/nodemcu/car1", data)
    time.sleep(1)  # Adjust delay between messages as needed

mqtt_client.disconnect()
